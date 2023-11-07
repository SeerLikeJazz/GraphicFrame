from ui import Ui_MainWindow
from PySide6.QtWidgets import QMainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    from PySide6.QtCore import Slot
    from PySide6.QtGui import QCloseEvent
    from PySide6.QtWidgets import QAbstractButton
    import numpy as np
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.emg_channels = 32
        # self.imu_channels = 6 if self.checkBox_imu.isChecked() else 0
        # self.checkBox_vib.setVisible(False)
        self.fs = 500
        self.frames_per_imu = 9

        ts = 5  # seconds
        vs = 50  # uV
        self.GroupBox_signal.setTitle(
            "EMG Signal({}\u00b5V/Div-{}s/page)".format(int(vs), ts)
        )
        self.emg_plot = EmgPlot(
            fs=self.fs,
            channels=self.emg_channels,
            imu_channels=0,
            fpi=self.frames_per_imu,
            ts=ts,
            vs=vs,
        )

        self.data_timer = QTimer(self)
        self.data_timer.timeout.connect(self.process_data)
        self.emg_watchdog_timer = QTimer(self)
        self.emg_watchdog_timer.timeout.connect(self.emg_watchdog)
        self.stackedWidget.setCurrentIndex(0)
        self.socket_flag = Value("i", 0)
        self.armband = None

        self.on_comboBox_highpass_currentIndexChanged()
        self.on_comboBox_lowpass_currentIndexChanged()
        self.on_comboBox_notch_currentIndexChanged()



    def process_data(self):
        data_frames = np.array(self.armband.get_data(), dtype=np.float32)
        if len(data_frames) == 0:
            return

        data_frames[:, : self.emg_channels] = (
            data_frames[:, : self.emg_channels] * 0.02235174
        )
        plotdata = self.filt_data(data_frames)

        for frame, plot in zip(data_frames, plotdata):
            self.emg_plot.update_data(plot)



    @Slot(bool)
    def on_pushButton_connect_toggled(self, checked):
        if checked:
            # port = iArmBand.get_device()
            port = "COM47"
            if port is not None:
                self.pushButton_connect.setText("Disconnect")
                self.armband = iArmBand(
                    port,
                    self.socket_flag,
                    imu=self.checkBox_imu.isChecked(),
                    vib=self.checkBox_vib.isChecked(),
                )
                self.armband.start()
                self.battery_value = -1
                self.checkBox_imu.setEnabled(False)
                self.checkBox_vib.setEnabled(False)
                self.data_timer.start(15)
                self.emg_watchdog_timer.start(500)
                self.label_2.setText(
                    "Connection successfully established: " + str(port)
                )
            else:
                QMessageBox.information(
                    self,
                    "Warning",
                    "No device found, please make sure receiver is plugged in.",
                )
                self.pushButton_connect.setChecked(False)

        else:
            self.data_timer.stop()
            self.emg_watchdog_timer.stop()
            self.pushButton_connect.setText("Connect")
            self.label_battery.setText("")
            self.checkBox_imu.setEnabled(True)
            self.checkBox_vib.setEnabled(True)
            if self.armband is not None:
                self.armband.close_cap()
                self.armband.terminate()
                self.armband = None
                self.label_2.setText("Welcome to use eCon smart EMG armband")

    def emg_watchdog(self):
        if self.socket_flag.value in [0, 1]:
            return
        elif self.socket_flag.value == 2:
            bat = self.armband.get_battery_value()
            if (self.battery_value != bat) and (bat >= 0) and (bat <= 100):
                self.battery_value = bat
                self.label_battery.setText("{}%".format(self.battery_value))
                if self.battery_value > 20:
                    self.label_battery.setStyleSheet("color: black")
                else:
                    self.label_battery.setStyleSheet("color: red")
        else:
            if self.socket_flag.value == 3:
                warn = "Data transmission timeout"
            elif self.socket_flag.value == 4:
                warn = "Please power up armband and try again."
            elif self.socket_flag.value == 5:
                warn = "Heartbeat package sent failed"
            elif self.socket_flag.value == 6:
                warn = "Error, closing connection"
            elif self.socket_flag.value == 9:
                warn = "Recv buffer full"
            else:
                warn = (
                    "Connection lost, please contact developer,\nSocket flag: "
                    + str(self.socket_flag.value)
                )
            self.socket_flag.value = 0
            QMessageBox.information(self, "Warning", warn + ", please reconnect.")
            self.pushButton_connect.setChecked(False)


### 页面切换
    @Slot(QAbstractButton)
    def on_buttonGroup_buttonClicked(self, button):
        self.emg_plot.resize(1, 1)
        if button == self.pushButton_menu_connect:
            self.stackedWidget.setCurrentWidget(self.page_connect)
        elif button == self.pushButton_menu_signal:
            self.gridLayout_plot.addWidget(self.emg_plot)
            self.stackedWidget.setCurrentWidget(self.page_signal)
    #     elif button == self.pushButton_menu_train:
    #         self.ges_manager.set_gestures(self.horizontalLayout_7, True)
    #         self.ges_manager.set_focus(0)
    #         self.gridLayout_sig.addWidget(self.emg_plot)
    #         self.stackedWidget.setCurrentWidget(self.page_train)
    #     elif button == self.pushButton_menu_test:
    #         self.stackedWidget.setCurrentWidget(self.page_test)
    #         self.ges_manager.set_gestures(self.horizontalLayout_5, False)
    #     elif button == self.pushButton_menu_control:
    #         self.stackedWidget.setCurrentWidget(self.page_application)
    #     elif button == self.pushButton_menu_about:
    #         self.stackedWidget.setCurrentWidget(self.page_about)

    @Slot()
    def on_comboBox_highpass_currentIndexChanged(self):
        self.highpass = eval(self.comboBox_highpass.currentText())
        if self.highpass is not None:
            Wnh = self.highpass / (self.fs / 2)
            self.filter_bh, self.filter_ah = butter(5, Wnh, btype="high")
            zih = lfilter_zi(self.filter_bh, self.filter_ah)
            self.zih = [zih for _ in range(self.emg_channels)]

    @Slot()
    def on_comboBox_notch_currentIndexChanged(self):
        self.notch = eval(self.comboBox_notch.currentText())
        if self.notch is not None:
            self.notch_b, self.notch_a = iirnotch(w0=self.notch, Q=30.0, fs=self.fs)
            notch_zi = lfilter_zi(self.notch_b, self.notch_a)
            self.notch_zi = [notch_zi for _ in range(self.emg_channels)]

    @Slot()
    def on_comboBox_lowpass_currentIndexChanged(self):
        self.lowpass = eval(self.comboBox_lowpass.currentText())
        if self.lowpass is not None:
            Wnl = self.lowpass / (self.fs / 2)
            self.filter_bl, self.filter_al = butter(4, Wnl, btype="low")
            zil = lfilter_zi(self.filter_bl, self.filter_al)
            self.zil = [zil for _ in range(self.emg_channels)]

    def filt_data(self, data: np.ndarray):
        plotdata = copy.deepcopy(data.T)
        if self.notch is not None:
            for i in range(self.emg_channels):  # notch filter
                plotdata[i, :], self.notch_zi[i] = lfilter(
                    self.notch_b, self.notch_a, plotdata[i, :], zi=self.notch_zi[i]
                )
        if self.highpass is not None:
            for i in range(self.emg_channels):
                plotdata[i, :], self.zih[i] = lfilter(
                    self.filter_bh, self.filter_ah, plotdata[i, :], zi=self.zih[i]
                )
        if self.lowpass is not None:
            for i in range(self.emg_channels):
                plotdata[i, :], self.zil[i] = lfilter(
                    self.filter_bl, self.filter_al, plotdata[i, :], zi=self.zil[i]
                )
        return plotdata.T


    def closeEvent(self, event: QCloseEvent) -> None:
        # reply = QMessageBox.question(
        #     self,
        #     "Message",
        #     "Do you want to close the application?",
        #     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        #     QMessageBox.StandardButton.No,
        # )
        # if reply == QMessageBox.StandardButton.Yes:
        if self.pushButton_connect.isChecked():
            self.on_pushButton_connect_toggled(False)
        event.accept()
        # else:
        #     event.ignore()


if __name__ == "__main__":
    from multiprocessing import freeze_support

    freeze_support()
    import sys, os
    import re, time, copy, traceback
    from multiprocessing import Value

    import numpy as np
    from scipy.signal import iirnotch, lfilter_zi, lfilter, butter
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import QTimer,QPropertyAnimation,QEasingCurve
    from PySide6.QtGui import QIcon
    from PySide6.QtWidgets import (
        QMessageBox,
        QMainWindow,
    )
    from signal_plot import EmgPlot
    from armband import iArmBand

    # os.chdir(os.path.dirname(os.path.abspath(__file__))) #for mac use
    print("Starting eConAlpha, please wait ...")
    # with open("resources/qss/blue.txt") as file:
    #     qss = "".join(file.readlines()).strip("\n")
    app = QApplication()
    # app.setStyleSheet(qss)
    app.setWindowIcon(QIcon("logo.ico"))
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
