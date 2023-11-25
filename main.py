from ui import Ui_MainWindow
from PySide6.QtWidgets import QMainWindow
from armband.device_socket import UsbCDC_socket as device_socket

class MainWindow(QMainWindow, Ui_MainWindow):
    from PySide6.QtCore import Slot
    from PySide6.QtGui import QCloseEvent
    from PySide6.QtWidgets import QAbstractButton
    import numpy as np

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.eeg_channels = 32
        self.fs = 500
        timescale = 5  # seconds
        vertscale = 50  # uV
        self.GroupBox_signal.setTitle(
            "EEG Signal({}\u00b5V/Div-{}s/page)".format(int(vertscale), timescale)
        )
        self.eeg_plot = SigPlot(
            fs=self.fs,
            channels=self.eeg_channels,
            timescale=timescale,
            vertscale=vertscale,
        )

        self.data_timer = QTimer(self)
        self.data_timer.timeout.connect(self.process_data)
        self.eeg_watchdog_timer = QTimer(self)
        self.eeg_watchdog_timer.timeout.connect(self.emg_watchdog) # 更新电量、设置按钮状态
        self.stackedWidget.setCurrentIndex(0)
        self.socket_flag = Value("i", 0)
        self.iRecorder = None

        self.on_comboBox_highpass_currentIndexChanged()
        self.on_comboBox_lowpass_currentIndexChanged()
        self.on_comboBox_notch_currentIndexChanged()
        # 把画布打开
        self.gridLayout_plot.addWidget(self.eeg_plot)
        self.stackedWidget.setCurrentWidget(self.page_signal)

        self.devicePort = None
        self.listWidget.clicked.connect(self.listclicked) # Port列表点击事件
        self.pushButton_start.setEnabled(False)  # 失能start按钮（置灰）
        self.pushButton_connect.setEnabled(False)  # 失能connect按钮（置灰）

    # 按键
    @Slot()
    def on_pushButton_search_clicked(self):
        self.pushButton_connect.setEnabled(False)  # 失能按钮（置灰）
        self.listWidget.clear() # 清除列表
        ports = MyDevice.get_device()
        for port in ports:
            self.listWidget.addItem(port.description)

    def listclicked(self):
        self.devicePort = self.listWidget.currentItem().text()[10:-1]
        print(self.listWidget.currentItem().text()[10:-1])
        self.pushButton_connect.setEnabled(True)  # 使能connect按钮

    @Slot(bool)
    def on_pushButton_connect_toggled(self, checked):
        if checked:
            port = self.devicePort
            if port is not None:
                self.pushButton_connect.setText("Connecting")
                self.iRecorder = MyDevice(
                    port,
                    self.socket_flag,
                )
                self.iRecorder.start()
                self.battery_value = -1  # connect的时候就显示电量
                self.eeg_watchdog_timer.start(500)
            else:
                QMessageBox.information(
                    self,
                    "Warning",
                    "No device found, please make sure receiver is plugged in.",
                )
                self.pushButton_connect.setChecked(False)
        else:
            self.data_timer.stop()
            self.eeg_watchdog_timer.stop()
            self.iRecorder.stop_acquisition()  # 设置进程run的状态，发送'R'指令
            self.pushButton_start.setText("Start")
            self.label_battery.setText("")
            self.pushButton_connect.setText("Connect")
            self.pushButton_search.setEnabled(True)  # 使能search按钮
            self.pushButton_start.setEnabled(False)  # 失能start按钮
            if self.iRecorder is not None:
                self.iRecorder.close_cap()
                self.iRecorder.terminate()
                self.iRecorder = None

    # 按键
    @Slot(bool)
    def on_pushButton_start_toggled(self, checked):
        if checked:
            self.iRecorder.start_acquisition_data()
            self.data_timer.start(15)
            self.pushButton_start.setText("Stop")
        else:
            self.data_timer.stop()
            self.pushButton_start.setText("Start")
            self.iRecorder.stop_acquisition()

    def process_data(self):
        data_frames = np.array(self.iRecorder.get_data(), dtype=np.float32)
        if len(data_frames) == 0:
            return

        data_frames[:, : self.eeg_channels] = (
            data_frames[:, : self.eeg_channels] * 0.02235174
        )
        plotdata = self.filt_data(data_frames)

        for frame, plot in zip(data_frames, plotdata):
            self.eeg_plot.update_data(plot)

    def emg_watchdog(self):
        if self.socket_flag.value in [0, 1]:
            return
        elif self.socket_flag.value == 2:
            self.pushButton_connect.setText("Disconnect")
            self.pushButton_start.setEnabled(True)  # 使能start按钮
            self.pushButton_search.setEnabled(False)  # 失能search按钮
            bat = self.iRecorder.get_battery_value()
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
                warn = "Please power up iRecorder and try again."
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


    @Slot()
    def on_comboBox_highpass_currentIndexChanged(self):
        self.highpass = eval(self.comboBox_highpass.currentText())
        if self.highpass is not None:
            Wnh = self.highpass / (self.fs / 2)
            self.filter_bh, self.filter_ah = butter(5, Wnh, btype="high")
            zih = lfilter_zi(self.filter_bh, self.filter_ah)
            self.zih = [zih for _ in range(self.eeg_channels)]

    @Slot()
    def on_comboBox_notch_currentIndexChanged(self):
        self.notch = eval(self.comboBox_notch.currentText())
        if self.notch is not None:
            self.notch_b, self.notch_a = iirnotch(w0=self.notch, Q=30.0, fs=self.fs)
            notch_zi = lfilter_zi(self.notch_b, self.notch_a)
            self.notch_zi = [notch_zi for _ in range(self.eeg_channels)]

    @Slot()
    def on_comboBox_lowpass_currentIndexChanged(self):
        self.lowpass = eval(self.comboBox_lowpass.currentText())
        if self.lowpass is not None:
            Wnl = self.lowpass / (self.fs / 2)
            self.filter_bl, self.filter_al = butter(4, Wnl, btype="low")
            zil = lfilter_zi(self.filter_bl, self.filter_al)
            self.zil = [zil for _ in range(self.eeg_channels)]

    def filt_data(self, data: np.ndarray):
        plotdata = copy.deepcopy(data.T)
        if self.notch is not None:
            for i in range(self.eeg_channels):  # notch filter
                plotdata[i, :], self.notch_zi[i] = lfilter(
                    self.notch_b, self.notch_a, plotdata[i, :], zi=self.notch_zi[i]
                )
        if self.highpass is not None:
            for i in range(self.eeg_channels):
                plotdata[i, :], self.zih[i] = lfilter(
                    self.filter_bh, self.filter_ah, plotdata[i, :], zi=self.zih[i]
                )
        if self.lowpass is not None:
            for i in range(self.eeg_channels):
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
    from signal_plot import SigPlot
    from armband import MyDevice

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
