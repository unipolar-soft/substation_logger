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

dictConfig(DIC_LOGGING_CONFIG)
logger = logging.getLogger(conf.LOGGER_NAME)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.db = DB()
        self.load_ui()

    def load_ui(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.tabs = QTabWidget(self)

        self.tabs.addTab(OpcWindow(self.db), "OPC Conf")

        self.setCentralWidget(self.tabs)

        menuConnection = self.ui.menubar.addMenu("Connection")
        action = menuConnection.addAction("API Adapter")
        action.triggered.connect(self.netInterfaceSelection)
    
    def netInterfaceSelection(self):
        print("Network interface selection")
        interfaces = psutil.net_if_addrs()
        interface_name_list = list(interfaces.keys())
        item, ok = QInputDialog.getItem(self, "Select API Interface",
                                "Interface", interface_name_list, 0, False )
        if ok and item:
            print(interfaces[item][1].address)
            db = DB()
            db.update_or_insert_keyValue(conf.KEY_API_ADAPTER, item)
