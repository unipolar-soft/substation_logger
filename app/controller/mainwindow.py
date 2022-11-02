# This Python file uses the following encoding: utf-8
from tkinter import dialog
import psutil
import logging
from logging.config import dictConfig

from PySide6.QtWidgets import QMainWindow, QTabWidget, QInputDialog

from app.db.database import DB
from ..ui.ui_mainwindow import Ui_MainWindow
from ..projutil.log_conf import DIC_LOGGING_CONFIG
from ..projutil import conf
from .opcwindow import OpcWindow
from .dashboard import DashBoard

dictConfig(DIC_LOGGING_CONFIG)
logger = logging.getLogger(conf.LOGGER_NAME)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.db = DB()
        self.load_ui()

        adapter = self.db.get_value_from_key(conf.KEY_API_ADAPTER)
        if not adapter:
            self.db.update_or_insert_keyValue(conf.KEY_API_ADAPTER, "Ethernet")

    def load_ui(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.tabs = QTabWidget(self)
        self.tabs.addTab(OpcWindow(self.db), "OPC Conf")
        self.tabs.addTab(DashBoard(self.db), "DashBoard")
        self.setCentralWidget(self.tabs)

        menuConnection = self.ui.menubar.addMenu("Connection")
        action = menuConnection.addAction("API Adapter")
        action.triggered.connect(self.netInterfaceSelection)
      
    
    def netInterfaceSelection(self):
        prev_adap = self.db.get_value_from_key(conf.KEY_API_ADAPTER)
        index = 0
        interfaces = psutil.net_if_addrs()
        interface_name_list = list(interfaces.keys())
        try:
            index = interface_name_list.index(prev_adap)
        except ValueError:
            logger.info("Previousl Selected Adapter Not Found")
        item, ok = QInputDialog.getItem(self, "Select API Interface",
                                "Interface", interface_name_list, index, False )
        if ok and item:
            self.db.update_or_insert_keyValue(conf.KEY_API_ADAPTER, item)
            logger.info(f"API Adapter Changed to {item}")
