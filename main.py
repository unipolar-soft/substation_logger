# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon
from app.controller.mainwindow import MainWindow
from app.projutil.util import show_message
from app.db.utils import is_db_available, getDBConf
from app.controller.dbconfcontroller import DBConf
from PySide6.QtGui import QIcon, QPixmap
from app.controller.systemtray import SystemTrayIcon

from app.res import icons

def launchMainWindow(app):
    
    widget = MainWindow()
    trayicon = SystemTrayIcon(QIcon(QPixmap(':/icons/logo5.png')), app, widget)
    trayicon.show()
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
    QApplication.setApplicationDisplayName("Storian by Unipolar")
    QApplication.setWindowIcon(QIcon(QPixmap(':/icons/logo5.png')))
    app.setQuitOnLastWindowClosed(False)
    main(app)
    
