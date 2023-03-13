# This Python file uses the following encoding: utf-8
import os
import json
from pathlib import Path
import sys

from PySide6.QtWidgets import QApplication
from  PySide6.QtCore import QSettings
from app.controller.mainwindow import MainWindow
from app.projutil.util import show_message
from app.db.utils import is_db_available, getDBConf
from app.controller.dbconfcontroller import DBConf

def launchMainWindow(app):
    
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())

def main(app):
    confs = getDBConf()
    if confs:
        res, msg = is_db_available(
                host = confs["host"], 
                port = confs["port"], 
                user = confs["user"], 
                password = confs["password"], 
                dbname = confs["db_name"]
                )
        if res:  
            launchMainWindow(app)
        else:
            msg = msg.split(":")[-1]
            res = show_message(f"Database Connection Could not be made!\n {msg}")
            conf = DBConf()
            res = conf.exec()
            if res:
                main(app)
    else:
        conf = DBConf()
        res = conf.exec()
        if res:
            main(app)

if __name__ == "__main__":
    app = QApplication([])
    QApplication.setOrganizationName("unipolar.com.bd")
    QApplication.setApplicationName("SubLogger")
    main(app)
    
