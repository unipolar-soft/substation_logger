# This Python file uses the following encoding: utf-8
import os
import json
from pathlib import Path
import sys

from PySide6.QtWidgets import QApplication
from  PySide6.QtCore import QSettings
from app.controller.mainwindow import MainWindow
from app.projutil.util import show_message
from app.db.utils import is_db_available
from app.controller.dbconfcontroller import DBConf

def getDBConfAvailable():
        '''
        checks if application configaration file already contains 
        a db connection parameters
        '''
        # filepath = "./app/db/db_con.json"
        # if os.path.isfile(filepath):
        #     with open(filepath) as f:
        #         js = json.load(f)
        #         return js
        # else:
        #     return False
        settings =  QSettings()
        host = settings.value("host", None)
        port = settings.value("port", None)
        user = settings.value("user", None)
        password = settings.value("password", None)
        db_name = settings.value("db_name", None)

        if host and port and user and password and db_name:
            return {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "db_name":  db_name
        }
        else:
            return False

def launchMainWindow(app):
    
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())

def main(app):
    confs = getDBConfAvailable()
    if confs:
        if is_db_available(
                host = confs["host"], 
                port = confs["port"], 
                user = confs["user"], 
                password = confs["password"], 
                dbname = confs["db_name"]
                ):  
            launchMainWindow(app)
        else:
            res = show_message("Database Connection Could not be made!")
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
    QApplication.setOrganizationName("Unipolar")
    QApplication.setApplicationName("SubLogger")
    main(app)
    
