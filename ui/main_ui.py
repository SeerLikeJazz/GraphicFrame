# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QButtonGroup, QComboBox, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLayout, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QVBoxLayout, QWidget)
from . import resource_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1085, 795)
        MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame_menu = QFrame(self.centralwidget)
        self.frame_menu.setObjectName(u"frame_menu")
        self.frame_menu.setMinimumSize(QSize(0, 500))
        self.frame_menu.setStyleSheet(u"text-align: left;")
        self.frame_menu.setFrameShape(QFrame.StyledPanel)
        self.frame_menu.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_menu)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_menu_logo = QLabel(self.frame_menu)
        self.label_menu_logo.setObjectName(u"label_menu_logo")
        self.label_menu_logo.setMinimumSize(QSize(100, 50))
        self.label_menu_logo.setMaximumSize(QSize(70, 50))
        self.label_menu_logo.setPixmap(QPixmap(u":/logos/resources/logo.png"))
        self.label_menu_logo.setScaledContents(True)
        self.label_menu_logo.setAlignment(Qt.AlignCenter)
        self.label_menu_logo.setMargin(3)

        self.verticalLayout.addWidget(self.label_menu_logo)

        self.pushButton_menu_connect = QPushButton(self.frame_menu)
        self.buttonGroup = QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.pushButton_menu_connect)
        self.pushButton_menu_connect.setObjectName(u"pushButton_menu_connect")
        self.pushButton_menu_connect.setMinimumSize(QSize(100, 50))
        icon = QIcon()
        icon.addFile(u":/icons/resources/icons/link-2.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_menu_connect.setIcon(icon)
        self.pushButton_menu_connect.setIconSize(QSize(20, 20))
        self.pushButton_menu_connect.setCheckable(True)
        self.pushButton_menu_connect.setChecked(True)

        self.verticalLayout.addWidget(self.pushButton_menu_connect)

        self.pushButton_menu_signal = QPushButton(self.frame_menu)
        self.buttonGroup.addButton(self.pushButton_menu_signal)
        self.pushButton_menu_signal.setObjectName(u"pushButton_menu_signal")
        self.pushButton_menu_signal.setMinimumSize(QSize(100, 50))
        icon1 = QIcon()
        icon1.addFile(u":/icons/resources/icons/bar-chart-2.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_menu_signal.setIcon(icon1)
        self.pushButton_menu_signal.setIconSize(QSize(20, 20))
        self.pushButton_menu_signal.setCheckable(True)

        self.verticalLayout.addWidget(self.pushButton_menu_signal)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.frame_battery = QFrame(self.frame_menu)
        self.frame_battery.setObjectName(u"frame_battery")
        self.frame_battery.setMinimumSize(QSize(50, 0))
        self.horizontalLayout_battery = QHBoxLayout(self.frame_battery)
        self.horizontalLayout_battery.setSpacing(1)
        self.horizontalLayout_battery.setObjectName(u"horizontalLayout_battery")
        self.horizontalLayout_battery.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout_battery.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.frame_battery)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(25, 25))
        self.label_3.setMaximumSize(QSize(24, 20))
        self.label_3.setPixmap(QPixmap(u":/icons/resources/icons/battery.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setTextInteractionFlags(Qt.NoTextInteraction)

        self.horizontalLayout_battery.addWidget(self.label_3, 0, Qt.AlignLeft|Qt.AlignVCenter)

        self.label_battery = QLabel(self.frame_battery)
        self.label_battery.setObjectName(u"label_battery")
        self.label_battery.setMinimumSize(QSize(25, 20))
        self.label_battery.setMaximumSize(QSize(30, 20))
        self.label_battery.setTextFormat(Qt.AutoText)
        self.label_battery.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_battery.setTextInteractionFlags(Qt.NoTextInteraction)

        self.horizontalLayout_battery.addWidget(self.label_battery, 0, Qt.AlignLeft|Qt.AlignVCenter)


        self.verticalLayout.addWidget(self.frame_battery, 0, Qt.AlignLeft)


        self.horizontalLayout.addWidget(self.frame_menu)

        self.frame_main = QFrame(self.centralwidget)
        self.frame_main.setObjectName(u"frame_main")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_main.sizePolicy().hasHeightForWidth())
        self.frame_main.setSizePolicy(sizePolicy)
        self.frame_main.setFrameShape(QFrame.StyledPanel)
        self.frame_main.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_main)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(self.frame_main)
        self.stackedWidget.setObjectName(u"stackedWidget")
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setLineWidth(0)
        self.page_connect = QWidget()
        self.page_connect.setObjectName(u"page_connect")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.page_connect.sizePolicy().hasHeightForWidth())
        self.page_connect.setSizePolicy(sizePolicy1)
        self.verticalLayout_2 = QVBoxLayout(self.page_connect)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_start_page = QVBoxLayout()
        self.verticalLayout_start_page.setObjectName(u"verticalLayout_start_page")
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_start_page.addItem(self.verticalSpacer_3)

        self.label_start_page = QLabel(self.page_connect)
        self.label_start_page.setObjectName(u"label_start_page")
        sizePolicy.setHeightForWidth(self.label_start_page.sizePolicy().hasHeightForWidth())
        self.label_start_page.setSizePolicy(sizePolicy)
        self.label_start_page.setPixmap(QPixmap(u":/logos/resources/econ.png"))
        self.label_start_page.setAlignment(Qt.AlignCenter)

        self.verticalLayout_start_page.addWidget(self.label_start_page)

        self.label = QLabel(self.page_connect)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(14)
        font.setBold(False)
        self.label.setFont(font)
        self.label.setLayoutDirection(Qt.LeftToRight)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_start_page.addWidget(self.label)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_start_page.addItem(self.verticalSpacer_2)

        self.horizontalFrame = QFrame(self.page_connect)
        self.horizontalFrame.setObjectName(u"horizontalFrame")
        self.verticalLayout_10 = QVBoxLayout(self.horizontalFrame)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.pushButton_connect = QPushButton(self.horizontalFrame)
        self.pushButton_connect.setObjectName(u"pushButton_connect")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pushButton_connect.sizePolicy().hasHeightForWidth())
        self.pushButton_connect.setSizePolicy(sizePolicy2)
        self.pushButton_connect.setMinimumSize(QSize(120, 40))
        self.pushButton_connect.setMaximumSize(QSize(120, 40))
        font1 = QFont()
        font1.setPointSize(11)
        self.pushButton_connect.setFont(font1)
        self.pushButton_connect.setInputMethodHints(Qt.ImhSensitiveData)
        icon2 = QIcon()
        icon2.addFile(u":/icons/resources/icons/link.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_connect.setIcon(icon2)
        self.pushButton_connect.setCheckable(True)

        self.verticalLayout_10.addWidget(self.pushButton_connect)


        self.verticalLayout_start_page.addWidget(self.horizontalFrame, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_start_page.addItem(self.verticalSpacer_4)

        self.verticalLayout_start_page.setStretch(0, 2)
        self.verticalLayout_start_page.setStretch(1, 2)
        self.verticalLayout_start_page.setStretch(5, 1)

        self.verticalLayout_2.addLayout(self.verticalLayout_start_page)

        self.stackedWidget.addWidget(self.page_connect)
        self.page_signal = QWidget()
        self.page_signal.setObjectName(u"page_signal")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.page_signal.sizePolicy().hasHeightForWidth())
        self.page_signal.setSizePolicy(sizePolicy3)
        self.verticalLayout_4 = QVBoxLayout(self.page_signal)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.GroupBox_signal = QGroupBox(self.page_signal)
        self.GroupBox_signal.setObjectName(u"GroupBox_signal")
        sizePolicy3.setHeightForWidth(self.GroupBox_signal.sizePolicy().hasHeightForWidth())
        self.GroupBox_signal.setSizePolicy(sizePolicy3)
        self.GroupBox_signal.setFocusPolicy(Qt.ClickFocus)
        self.GroupBox_signal.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.GroupBox_signal.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.horizontalLayout_4 = QHBoxLayout(self.GroupBox_signal)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_plot = QGridLayout()
        self.gridLayout_plot.setObjectName(u"gridLayout_plot")
        self.gridLayout_plot.setHorizontalSpacing(0)
        self.gridLayout_plot.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout_4.addLayout(self.gridLayout_plot)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox_filter = QGroupBox(self.GroupBox_signal)
        self.groupBox_filter.setObjectName(u"groupBox_filter")
        self.verticalLayout_11 = QVBoxLayout(self.groupBox_filter)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.label_4 = QLabel(self.groupBox_filter)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_11.addWidget(self.label_4)

        self.comboBox_highpass = QComboBox(self.groupBox_filter)
        self.comboBox_highpass.addItem("")
        self.comboBox_highpass.addItem("")
        self.comboBox_highpass.addItem("")
        self.comboBox_highpass.addItem("")
        self.comboBox_highpass.addItem("")
        self.comboBox_highpass.setObjectName(u"comboBox_highpass")

        self.verticalLayout_11.addWidget(self.comboBox_highpass)

        self.label_5 = QLabel(self.groupBox_filter)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_11.addWidget(self.label_5)

        self.comboBox_lowpass = QComboBox(self.groupBox_filter)
        self.comboBox_lowpass.addItem("")
        self.comboBox_lowpass.addItem("")
        self.comboBox_lowpass.addItem("")
        self.comboBox_lowpass.addItem("")
        self.comboBox_lowpass.setObjectName(u"comboBox_lowpass")

        self.verticalLayout_11.addWidget(self.comboBox_lowpass)

        self.label_6 = QLabel(self.groupBox_filter)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_11.addWidget(self.label_6)

        self.comboBox_notch = QComboBox(self.groupBox_filter)
        self.comboBox_notch.addItem("")
        self.comboBox_notch.addItem("")
        self.comboBox_notch.addItem("")
        self.comboBox_notch.setObjectName(u"comboBox_notch")

        self.verticalLayout_11.addWidget(self.comboBox_notch)


        self.verticalLayout_3.addWidget(self.groupBox_filter, 0, Qt.AlignTop)

        self.groupBox_record = QGroupBox(self.GroupBox_signal)
        self.groupBox_record.setObjectName(u"groupBox_record")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_record)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.pushButton_start = QPushButton(self.groupBox_record)
        self.pushButton_start.setObjectName(u"pushButton_start")
        sizePolicy2.setHeightForWidth(self.pushButton_start.sizePolicy().hasHeightForWidth())
        self.pushButton_start.setSizePolicy(sizePolicy2)
        self.pushButton_start.setMaximumSize(QSize(100, 30))
        icon3 = QIcon()
        icon3.addFile(u":/icons/resources/icons/play-circle.svg", QSize(), QIcon.Normal, QIcon.Off)
        icon3.addFile(u":/icons/resources/icons/stop-circle.svg", QSize(), QIcon.Normal, QIcon.On)
        self.pushButton_start.setIcon(icon3)
        self.pushButton_start.setCheckable(True)

        self.verticalLayout_7.addWidget(self.pushButton_start)


        self.verticalLayout_3.addWidget(self.groupBox_record)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_7)


        self.horizontalLayout_4.addLayout(self.verticalLayout_3)

        self.horizontalLayout_4.setStretch(0, 9)
        self.horizontalLayout_4.setStretch(1, 1)

        self.verticalLayout_4.addWidget(self.GroupBox_signal)

        self.verticalLayout_4.setStretch(0, 9)
        self.stackedWidget.addWidget(self.page_signal)

        self.gridLayout.addWidget(self.stackedWidget, 0, 0, 1, 1)


        self.horizontalLayout.addWidget(self.frame_main)

        self.horizontalLayout.setStretch(1, 5)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(1)
        self.comboBox_highpass.setCurrentIndex(2)
        self.comboBox_lowpass.setCurrentIndex(0)
        self.comboBox_notch.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"eConAlpha", None))
        self.label_menu_logo.setText("")
        self.pushButton_menu_connect.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.pushButton_menu_signal.setText(QCoreApplication.translate("MainWindow", u"Signal", None))
        self.label_3.setText("")
        self.label_battery.setText("")
        self.label_start_page.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Welcome to use iRecorder", None))
        self.pushButton_connect.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.GroupBox_signal.setTitle(QCoreApplication.translate("MainWindow", u"EMG Signal(100\u00b5V/Div-2s/page)", None))
        self.groupBox_filter.setTitle(QCoreApplication.translate("MainWindow", u"Filter", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"High Pass (Hz)", None))
        self.comboBox_highpass.setItemText(0, QCoreApplication.translate("MainWindow", u"None", None))
        self.comboBox_highpass.setItemText(1, QCoreApplication.translate("MainWindow", u"0.1", None))
        self.comboBox_highpass.setItemText(2, QCoreApplication.translate("MainWindow", u"1", None))
        self.comboBox_highpass.setItemText(3, QCoreApplication.translate("MainWindow", u"5", None))
        self.comboBox_highpass.setItemText(4, QCoreApplication.translate("MainWindow", u"20", None))

        self.comboBox_highpass.setCurrentText(QCoreApplication.translate("MainWindow", u"1", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Low Pass (Hz)", None))
        self.comboBox_lowpass.setItemText(0, QCoreApplication.translate("MainWindow", u"None", None))
        self.comboBox_lowpass.setItemText(1, QCoreApplication.translate("MainWindow", u"30", None))
        self.comboBox_lowpass.setItemText(2, QCoreApplication.translate("MainWindow", u"40", None))
        self.comboBox_lowpass.setItemText(3, QCoreApplication.translate("MainWindow", u"70", None))

        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Notch (Hz)", None))
        self.comboBox_notch.setItemText(0, QCoreApplication.translate("MainWindow", u"None", None))
        self.comboBox_notch.setItemText(1, QCoreApplication.translate("MainWindow", u"50", None))
        self.comboBox_notch.setItemText(2, QCoreApplication.translate("MainWindow", u"60", None))

        self.groupBox_record.setTitle(QCoreApplication.translate("MainWindow", u"LSL", None))
        self.pushButton_start.setText(QCoreApplication.translate("MainWindow", u"Start", None))
    # retranslateUi

