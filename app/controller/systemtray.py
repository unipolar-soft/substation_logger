from PySide6.QtWidgets import QSystemTrayIcon, QApplication, QMenu
from app.controller.mainwindow import MainWindow
from PySide6.QtGui import QIcon, QPixmap
from app.res import icons

class SystemTrayIcon(QSystemTrayIcon):

    def __init__(self, icon:QIcon, parent:QApplication, mainwindow:MainWindow):

        super().__init__(icon, parent)

        self.menu = QMenu(mainwindow)
        open_action = self.menu.addAction("Open Substation Logger")
        open_action.triggered.connect(lambda : mainwindow.show())
        exit_Action = self.menu.addAction("Exit")
        exit_Action.triggered.connect(mainwindow.cleanClose)
        self.setContextMenu(self.menu)

        self.setToolTip('Feeder Break Historian')
        # Connect the activated signal to the slot
        self.activated.connect(self.onTrayIconActivated)
        
    def onTrayIconActivated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            # Handle the double-click event here
            self.menu.actions()[0].trigger()