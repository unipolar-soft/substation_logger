# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
import logging
from logging.config import dictConfig


from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect, QEvent, Signal,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon, QContextMenuEvent,
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
from ..component.tableview import TableViewWithContext
from ..opc import opcutils
from ..opc.opc import OpcuaClient

dictConfig(DIC_LOGGING_CONFIG)
logger = logging.getLogger(conf.LOGGER_NAME)

class OpcWindow(QWidget):
    def __init__(self, db: DB, opcClient: OpcuaClient):
        super(OpcWindow, self).__init__()  

        self.setWindowTitle("OPC Configuration")    
        self.db = db
        self.opcClient = opcClient
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
        # self.ui.linkEdit.editingFinished.connect(self.linkEditChanged)
        self.ui.opcConnectBtn.clicked.connect(self.connectOPC)

        self.ui.urlEditBtn.clicked.connect(self.urlEditClicked)
        # self.ui.linkEditBtn.clicked.connect(self.linkeditClicked)

        self.opcClient.opcConnectionStateChanged.connect(self.showConnect)

        self.substation_update_running = False
        self.tag_update_running = False

    def showConnect(self, state):
        styel = ''
        if state:
            styel = "background:rgb(0, 170, 127)"
            self.ui.opcConnectBtn.setText("Disconnect")
        else:
            styel = "background:rgb(85, 90, 89)"
            self.ui.opcConnectBtn.setText("Connect")

        self.ui.connectionIndicator.setStyleSheet(styel)

    
    def connectionIndicatorStyling(self, state):
        if state:
            styelIndicator = "background:rgb(0, 170, 127)"
            styleUrl = "border: 3px solid green"
        else:
            styelIndicator = "background:rgb(85, 90, 89)"
            styleUrl = "border: 3px solid red"
        # self.ui.connectionIndicator.setStyleSheet(styelIndicator)
        self.ui.urlEdit.setStyleSheet(styleUrl)

    def connectOPC(self):
        if self.opcClient.is_alive():
            self.opcClient.stop_service()
        else:
            sucess, msg = self.opcClient.start_service()
            if not sucess:
                show_message(msg)  

    def loadValues(self):
        url = self.db.get_value_from_key(conf.KEY_URL)
        self.ui.urlEdit.setText(url)
        self.ui.urlEdit.setReadOnly(True)
        res = opcutils.testUrl(url)
        self.connectionIndicatorStyling(res[0])

        link = self.db.get_value_from_key(conf.KEY_LINK)
        # self.ui.linkEdit.setText(link)
        # self.ui.linkEdit.setReadOnly(True)

    # def linkeditClicked(self):
    #     self.ui.linkEdit.setReadOnly(False)
    #     self.ui.linkEdit.setFocus()
    
    def urlEditClicked(self):
        self.ui.urlEdit.setReadOnly(False)
        self.ui.urlEdit.setFocus()

    def urlChanged(self):
        newUrl = self.ui.urlEdit.text()
        logger.info(f"url set to {newUrl}")

        if newUrl != "":
            res = opcutils.testUrl(newUrl)
            self.connectionIndicatorStyling(res[0])   
            if not res[0]:
                show_message(str(res[1]))
                
                return
            self.ui.urlEdit.setReadOnly(True)
            self.db.update_or_insert_keyValue(conf.KEY_URL, newUrl)
    
    # def linkEditChanged(self):
    #     text = self.ui.linkEdit.text()
    #     logger.info(f"New prefix added: {text}")
    #     self.db.update_or_insert_keyValue(conf.KEY_LINK, text)

    #     self.ui.linkEdit.setReadOnly(True)
    
    def addSubStation(self):
        stationName = self.ui.stationNameEdit.text()
        stationPath = self.ui.stationPathEdit.text()
        stationPrefix = self.ui.stationPrefixEdit.text()

        if stationPath == '':
            show_message("Station Path must be Provided")
            return
        if stationPrefix == '':
            show_message("Station Prefix must be Provided")
            return
        if self.substation_update_running:
            substation = self.db.update_substation(stationName, stationPath, stationPrefix)
            self.ui.substationAddBtn.setText("Add")
            self.substation_update_running = False
        else: 
            substation = self.db.add_substation(stationName, stationPath, stationPrefix)
        
        self.substationModel.select()
        self.ui.stationNameEdit.setText("")
        self.ui.stationPathEdit.setText("")
        self.ui.stationPrefixEdit.setText("")
        self.opcClient.subscribe_new_station(substation)
    
    def editSubstation(self, row):
        name = self.substationModel.index(row, 0).data()
        path = self.substationModel.index(row, 1).data()
        prefix = self.substationModel.index(row, 2).data()

        self.ui.stationNameEdit.setText(name)
        self.ui.stationPathEdit.setText(path)
        self.ui.stationPrefixEdit.setText(prefix)

        self.ui.substationAddBtn.setText("Update")
        self.substation_update_running = True

    
    def deleteSubStation(self, row):
        name = self.substationModel.index(row, 0).data()
        path = self.substationModel.index(row, 1).data()
        prefix = self.substationModel.index(row, 2).data()

        self.db.delete_substation(name, path, prefix)

        self.substationModel.select()
    
    def addTag(self):
        tagName = self.ui.tagNameEdit.text()
        tagPath = self.ui.tagPathEdit.text()
        isMonitored = self.ui.tagMonitorCheckBtn.isChecked()

        if tagPath == '':
            show_message("Tag Path must be Provided")
            return
        if self.tag_update_running:
            self.db.update_tag(tagName, tagPath, isMonitored)
            self.ui.tagAddBtn.setText("Add")
            self.tag_update_running = False
        else:
            self.db.add_tag(tagName, tagPath, isMonitored)
        self.ui.tagNameEdit.setText("")
        self.ui.tagPathEdit.setText("")
        self.ui.tagMonitorCheckBtn.setChecked(False)
        self.tagsModel.select()

    def editTag(self, row):
        name = self.tagsModel.index(row, 0).data()
        path = self.tagsModel.index(row, 1).data()
        isMonitored = self.tagsModel.index(row, 2).data()

        self.ui.tagNameEdit.setText(name)
        self.ui.tagPathEdit.setText(path)
        self.ui.tagMonitorCheckBtn.setChecked(bool(isMonitored))

        self.ui.tagAddBtn.setText("Update")
        self.tag_update_running = True

    def deleteTag(self, row):
        name = self.tagsModel.index(row, 0).data()
        path = self.tagsModel.index(row, 1).data()

        self.db.delete_tag(name, path)

        self.tagsModel.select()

    def setupStationTable(self):
        self.substationModel = TableModel(SubStation)

        tableView = TableViewWithContext(self.substationModel)
        self.ui.stationTableLayout.addWidget(tableView)

        tableView.editSig.connect(lambda x: self.editSubstation(x))
        tableView.deleteSig.connect(lambda x: self.deleteSubStation(x))

    def setupTagTable(self):
        self.tagsModel = TableModel(Tags)
        tableView = TableViewWithContext(self.tagsModel)
        self.ui.tagTableLayout.addWidget(tableView)

        tableView.editSig.connect(lambda x: self.editTag(x))
        tableView.deleteSig.connect(lambda x: self.deleteTag(x))
    
    def setIcons(self):
            icon = QIcon(QPixmap(":/icons/edit.png"))
            self.ui.urlEditBtn.setIcon(icon)
            # self.ui.linkEditBtn.setIcon(icon)