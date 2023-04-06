# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dbconf.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QFormLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_DBConf(object):
    def setupUi(self, DBConf):
        if not DBConf.objectName():
            DBConf.setObjectName(u"DBConf")
        DBConf.resize(555, 388)
        DBConf.setMaximumSize(QSize(555, 388))
        self.buttonBox = QDialogButtonBox(DBConf)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(10, 340, 531, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.formLayoutWidget = QWidget(DBConf)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(10, 50, 531, 221))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.formLayoutWidget)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.hostEdit = QLineEdit(self.formLayoutWidget)
        self.hostEdit.setObjectName(u"hostEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.hostEdit)

        self.label_2 = QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.label_3 = QLabel(self.formLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.portEdit = QLineEdit(self.formLayoutWidget)
        self.portEdit.setObjectName(u"portEdit")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.portEdit)

        self.userEdit = QLineEdit(self.formLayoutWidget)
        self.userEdit.setObjectName(u"userEdit")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.userEdit)

        self.label_4 = QLabel(self.formLayoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_4)

        self.passwordEdit = QLineEdit(self.formLayoutWidget)
        self.passwordEdit.setObjectName(u"passwordEdit")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.passwordEdit)

        self.label_5 = QLabel(self.formLayoutWidget)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_5)

        self.dbnameEdit = QLineEdit(self.formLayoutWidget)
        self.dbnameEdit.setObjectName(u"dbnameEdit")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.dbnameEdit)

        self.dbms_label = QLabel(self.formLayoutWidget)
        self.dbms_label.setObjectName(u"dbms_label")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.dbms_label)

        self.dbms_select_comboBox = QComboBox(self.formLayoutWidget)
        self.dbms_select_comboBox.setObjectName(u"dbms_select_comboBox")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.dbms_select_comboBox)

        self.label_6 = QLabel(DBConf)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(160, 20, 231, 31))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_6.setFont(font)
        self.con_msg = QLabel(DBConf)
        self.con_msg.setObjectName(u"con_msg")
        self.con_msg.setGeometry(QRect(10, 289, 521, 41))
        self.label_7 = QLabel(DBConf)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(430, 280, 21, 29))
        self.label_7.setStyleSheet(u"background:rgb(182, 182, 182)")
        self.connectBtn = QPushButton(DBConf)
        self.connectBtn.setObjectName(u"connectBtn")
        self.connectBtn.setGeometry(QRect(460, 280, 80, 29))

        self.retranslateUi(DBConf)
        self.buttonBox.accepted.connect(DBConf.accept)
        self.buttonBox.rejected.connect(DBConf.reject)

        QMetaObject.connectSlotsByName(DBConf)
    # setupUi

    def retranslateUi(self, DBConf):
        DBConf.setWindowTitle(QCoreApplication.translate("DBConf", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("DBConf", u"Host", None))
        self.label_2.setText(QCoreApplication.translate("DBConf", u"Port", None))
        self.label_3.setText(QCoreApplication.translate("DBConf", u"User", None))
        self.label_4.setText(QCoreApplication.translate("DBConf", u"Password", None))
        self.label_5.setText(QCoreApplication.translate("DBConf", u"DB Name", None))
        self.dbms_label.setText(QCoreApplication.translate("DBConf", u"DBMS", None))
        self.label_6.setText(QCoreApplication.translate("DBConf", u"Database Configuration", None))
        self.con_msg.setText("")
        self.label_7.setText("")
        self.connectBtn.setText(QCoreApplication.translate("DBConf", u"Test", None))
    # retranslateUi

