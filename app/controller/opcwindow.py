# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
import logging
from logging.config import dictConfig


from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
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
from ..projutil.conf import LOGGER_NAME
from ..projutil.util import show_message
from ..db.database import DB
from ..db.tables import SubStation, Tags
from ..models.tablemodel import TableModel
dictConfig(DIC_LOGGING_CONFIG)
logger = logging.getLogger(LOGGER_NAME)

class OpcWindow(QWidget):
    def __init__(self, db: DB):
        super(OpcWindow, self).__init__()
        self.load_ui()
        self.db = db

    def load_ui(self):
        self.ui = Ui_OPCView()
        self.ui.setupUi(self)

        self.setupStationTable()
        self.setupTagTable()

        self.ui.substationAddBtn.clicked.connect(self.addSubStation)
        self.ui.tagAddBtn.clicked.connect(self.addTag)
    
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
