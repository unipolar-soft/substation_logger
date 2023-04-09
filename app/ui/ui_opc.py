# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'opc.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QGroupBox,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QWidget)

class Ui_OPCView(object):
    def setupUi(self, OPCView):
        if not OPCView.objectName():
            OPCView.setObjectName(u"OPCView")
        OPCView.resize(730, 727)
        self.groupBox = QGroupBox(OPCView)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(390, 70, 301, 621))
        self.groupBox_4 = QGroupBox(self.groupBox)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(10, 30, 281, 201))
        self.label_8 = QLabel(self.groupBox_4)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(10, 30, 51, 20))
        self.stationNameEdit = QLineEdit(self.groupBox_4)
        self.stationNameEdit.setObjectName(u"stationNameEdit")
        self.stationNameEdit.setGeometry(QRect(60, 30, 211, 28))
        self.label_9 = QLabel(self.groupBox_4)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(10, 70, 51, 20))
        self.stationPathEdit = QLineEdit(self.groupBox_4)
        self.stationPathEdit.setObjectName(u"stationPathEdit")
        self.stationPathEdit.setGeometry(QRect(60, 70, 211, 28))
        self.substationAddBtn = QPushButton(self.groupBox_4)
        self.substationAddBtn.setObjectName(u"substationAddBtn")
        self.substationAddBtn.setGeometry(QRect(192, 160, 51, 30))
        self.stationPrefixEdit = QLineEdit(self.groupBox_4)
        self.stationPrefixEdit.setObjectName(u"stationPrefixEdit")
        self.stationPrefixEdit.setGeometry(QRect(60, 110, 211, 28))
        self.label = QLabel(self.groupBox_4)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 110, 41, 20))
        self.formLayoutWidget_2 = QWidget(self.groupBox)
        self.formLayoutWidget_2.setObjectName(u"formLayoutWidget_2")
        self.formLayoutWidget_2.setGeometry(QRect(10, 240, 281, 371))
        self.stationTableLayout = QFormLayout(self.formLayoutWidget_2)
        self.stationTableLayout.setObjectName(u"stationTableLayout")
        self.stationTableLayout.setContentsMargins(0, 0, 0, 0)
        self.groupBox_2 = QGroupBox(OPCView)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(10, 70, 341, 621))
        self.groupBox_3 = QGroupBox(self.groupBox_2)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(10, 30, 301, 171))
        self.label_5 = QLabel(self.groupBox_3)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(10, 30, 51, 20))
        self.tagNameEdit = QLineEdit(self.groupBox_3)
        self.tagNameEdit.setObjectName(u"tagNameEdit")
        self.tagNameEdit.setGeometry(QRect(60, 30, 121, 28))
        self.label_4 = QLabel(self.groupBox_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 70, 51, 20))
        self.tagPathEdit = QLineEdit(self.groupBox_3)
        self.tagPathEdit.setObjectName(u"tagPathEdit")
        self.tagPathEdit.setGeometry(QRect(60, 70, 121, 28))
        self.tagMonitorCheckBtn = QCheckBox(self.groupBox_3)
        self.tagMonitorCheckBtn.setObjectName(u"tagMonitorCheckBtn")
        self.tagMonitorCheckBtn.setGeometry(QRect(60, 110, 93, 26))
        self.tagAddBtn = QPushButton(self.groupBox_3)
        self.tagAddBtn.setObjectName(u"tagAddBtn")
        self.tagAddBtn.setGeometry(QRect(220, 130, 51, 30))
        self.formLayoutWidget = QWidget(self.groupBox_2)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(9, 209, 321, 401))
        self.tagTableLayout = QFormLayout(self.formLayoutWidget)
        self.tagTableLayout.setObjectName(u"tagTableLayout")
        self.tagTableLayout.setContentsMargins(0, 0, 0, 0)
        self.urlLabel = QLabel(OPCView)
        self.urlLabel.setObjectName(u"urlLabel")
        self.urlLabel.setGeometry(QRect(10, 20, 63, 20))
        self.urlEdit = QLineEdit(OPCView)
        self.urlEdit.setObjectName(u"urlEdit")
        self.urlEdit.setGeometry(QRect(80, 20, 411, 30))
        self.urlEditBtn = QPushButton(OPCView)
        self.urlEditBtn.setObjectName(u"urlEditBtn")
        self.urlEditBtn.setGeometry(QRect(500, 20, 30, 30))
        self.groupBox_5 = QGroupBox(OPCView)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setGeometry(QRect(550, 0, 131, 61))
        self.opcConnectBtn = QPushButton(self.groupBox_5)
        self.opcConnectBtn.setObjectName(u"opcConnectBtn")
        self.opcConnectBtn.setGeometry(QRect(60, 30, 61, 30))
        self.connectionIndicator = QLabel(self.groupBox_5)
        self.connectionIndicator.setObjectName(u"connectionIndicator")
        self.connectionIndicator.setGeometry(QRect(20, 30, 31, 21))
        self.connectionIndicator.setStyleSheet(u"background:rgb(85, 90, 89)")

        self.retranslateUi(OPCView)

        QMetaObject.connectSlotsByName(OPCView)
    # setupUi

    def retranslateUi(self, OPCView):
        OPCView.setWindowTitle(QCoreApplication.translate("OPCView", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("OPCView", u"Substations", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("OPCView", u"Add Substation", None))
        self.label_8.setText(QCoreApplication.translate("OPCView", u"Name", None))
        self.label_9.setText(QCoreApplication.translate("OPCView", u"Path", None))
        self.substationAddBtn.setText(QCoreApplication.translate("OPCView", u"Add", None))
        self.label.setText(QCoreApplication.translate("OPCView", u"Prefix", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("OPCView", u"Tags", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("OPCView", u"Add Tag", None))
        self.label_5.setText(QCoreApplication.translate("OPCView", u"Name", None))
        self.label_4.setText(QCoreApplication.translate("OPCView", u"Path", None))
        self.tagMonitorCheckBtn.setText(QCoreApplication.translate("OPCView", u"Monitored", None))
        self.tagAddBtn.setText(QCoreApplication.translate("OPCView", u"Add", None))
        self.urlLabel.setText(QCoreApplication.translate("OPCView", u"URL", None))
        self.urlEditBtn.setText("")
        self.groupBox_5.setTitle(QCoreApplication.translate("OPCView", u"Connection", None))
        self.opcConnectBtn.setText(QCoreApplication.translate("OPCView", u"Connect", None))
        self.connectionIndicator.setText("")
    # retranslateUi

