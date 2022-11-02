# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
import logging
from logging.config import dictConfig


from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect, QEvent,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter, QIntValidator, QDoubleValidator,
    QPalette, QPixmap, QRadialGradient, QTransform, QAction)
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget, QMessageBox, QAbstractItemView,
    QMenu, QDialog, QDialogButtonBox, QVBoxLayout)

from ..ui.ui_opc import Ui_OPCView
from ..projutil.log_conf import DIC_LOGGING_CONFIG
from ..projutil import conf
from ..projutil.util import show_message
from ..db.database import DB
from ..db.tables import SubStation, Tags
from ..models.tablemodel import TableModel
from ..res import icons
dictConfig(DIC_LOGGING_CONFIG)
logger = logging.getLogger(conf.LOGGER_NAME)

class OpcWindow(QWidget):
    def __init__(self, db: DB):
        super(OpcWindow, self).__init__()      
        self.db = db
        self.load_ui()

    def load_ui(self):
        self.ui = Ui_OPCView()
        self.ui.setupUi(self)
        self.setIcons()

        self.setupStationTable()
        self.setupTagTable()
        self.loadValues()

        self.ui.substationAddBtn.clicked.connect(self.addSubStation)
        self.ui.tagAddBtn.clicked.connect(self.addTag)
        self.ui.urlEdit.editingFinished.connect(self.urlChanged)
        self.ui.linkEdit.editingFinished.connect(self.linkEditChanged)

        self.ui.urlEditBtn.clicked.connect(self.urlEditClicked)
        self.ui.linkEditBtn.clicked.connect(self.linkeditClicked)

    
    def loadValues(self):
        url = self.db.get_value_from_key(conf.KEY_URL)
        self.ui.urlEdit.setText(url)
        self.ui.urlEdit.setReadOnly(True)

        link = self.db.get_value_from_key(conf.KEY_LINK)
        self.ui.linkEdit.setText(link)
        self.ui.linkEdit.setReadOnly(True)

    def linkeditClicked(self):
        self.ui.linkEdit.setReadOnly(False)
        self.ui.linkEdit.setFocus()
    
    def urlEditClicked(self):
        self.ui.urlEdit.setReadOnly(False)
        self.ui.urlEdit.setFocus()

    def urlChanged(self):
        text = self.ui.urlEdit.text()
        self.db.update_or_insert_keyValue(conf.KEY_URL, text)
        logger.info(f"url set to {text}")

        self.ui.urlEdit.setReadOnly(True)
    
    def linkEditChanged(self):
        text = self.ui.linkEdit.text()
        logger.info(f"New prefix added: {text}")
        self.db.update_or_insert_keyValue(conf.KEY_LINK, text)

        self.ui.linkEdit.setReadOnly(True)
    
    def addSubStation(self):
        stationName = self.ui.stationNameEdit.text()
        stationPath = self.ui.stationPathEdit.text()

        if stationPath == '':
            show_message("Station Path must be Provided")
            return
        if self.db.add_substation(stationName, stationPath):
            self.ui.stationNameEdit.setText("")
            self.ui.stationPathEdit.setText("")
            self.substationModel.select()
    
    def addTag(self):
        tagName = self.ui.tagNameEdit.text()
        tagPath = self.ui.tagPathEdit.text()
        isMonitored = self.ui.tagMonitorCheckBtn.isChecked()

        if tagPath == '':
            show_message("Tag Path must be Provided")
            return
        if self.db.add_tag(tagName, tagPath, isMonitored):
            self.ui.tagNameEdit.setText("")
            self.ui.tagPathEdit.setText("")
            self.ui.tagMonitorCheckBtn.setChecked(False)
            self.tagsModel.select()

    def setupStationTable(self):
        self.substationModel = TableModel(SubStation)
        self.ui.substationTable.setModel(self.substationModel)
        self.ui.substationTable.setCornerButtonEnabled(False)
        self.ui.substationTable.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.ui.substationTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.substationTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.substationTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
    
    def setupTagTable(self):
        self.tagsModel = TableModel(Tags)
        self.ui.tagTable.setModel(self.tagsModel)
        self.ui.tagTable.setCornerButtonEnabled(False)
        self.ui.tagTable.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.ui.tagTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tagTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.tagTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
    
    def setIcons(self):
            icon = QIcon(QPixmap(":/icons/edit.png"))
            self.ui.urlEditBtn.setIcon(icon)
            self.ui.linkEditBtn.setIcon(icon)