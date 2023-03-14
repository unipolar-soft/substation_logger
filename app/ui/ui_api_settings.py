# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'api_settings.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QWidget)

class Ui_APIConfDialog(object):
    def setupUi(self, APIConfDialog):
        if not APIConfDialog.objectName():
            APIConfDialog.setObjectName(u"APIConfDialog")
        APIConfDialog.resize(640, 284)
        self.api_checkBox = QCheckBox(APIConfDialog)
        self.api_checkBox.setObjectName(u"api_checkBox")
        self.api_checkBox.setGeometry(QRect(50, 30, 281, 31))
        self.network_interface_Combobox = QComboBox(APIConfDialog)
        self.network_interface_Combobox.setObjectName(u"network_interface_Combobox")
        self.network_interface_Combobox.setGeometry(QRect(190, 70, 401, 28))
        self.label = QLabel(APIConfDialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(50, 70, 131, 21))
        self.label_2 = QLabel(APIConfDialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(50, 110, 131, 21))
        self.api_url_lineEdit = QLineEdit(APIConfDialog)
        self.api_url_lineEdit.setObjectName(u"api_url_lineEdit")
        self.api_url_lineEdit.setGeometry(QRect(190, 110, 401, 28))
        self.label_3 = QLabel(APIConfDialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(50, 150, 131, 20))
        self.data_format_Combobox = QComboBox(APIConfDialog)
        self.data_format_Combobox.setObjectName(u"data_format_Combobox")
        self.data_format_Combobox.setGeometry(QRect(190, 150, 401, 28))
        self.update_pushButton = QPushButton(APIConfDialog)
        self.update_pushButton.setObjectName(u"update_pushButton")
        self.update_pushButton.setGeometry(QRect(490, 210, 101, 29))
        self.update_message_level = QLabel(APIConfDialog)
        self.update_message_level.setObjectName(u"update_message_level")
        self.update_message_level.setGeometry(QRect(50, 210, 391, 31))

        self.retranslateUi(APIConfDialog)

        QMetaObject.connectSlotsByName(APIConfDialog)
    # setupUi

    def retranslateUi(self, APIConfDialog):
        APIConfDialog.setWindowTitle(QCoreApplication.translate("APIConfDialog", u"Dialog", None))
        self.api_checkBox.setText(QCoreApplication.translate("APIConfDialog", u"Push Tag Change to API", None))
        self.label.setText(QCoreApplication.translate("APIConfDialog", u"Network Interface", None))
        self.label_2.setText(QCoreApplication.translate("APIConfDialog", u"URL", None))
        self.label_3.setText(QCoreApplication.translate("APIConfDialog", u"Data Format", None))
        self.update_pushButton.setText(QCoreApplication.translate("APIConfDialog", u"UPDATE", None))
        self.update_message_level.setText("")
    # retranslateUi

