import logging
from logging.config import dictConfig
from ..projutil.log_conf import DIC_LOGGING_CONFIG
from ..projutil import conf

import  PySide6
from PySide6.QtWidgets import QTableView
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget, QMessageBox, QAbstractItemView,
    QMenu, QDialog, QDialogButtonBox, QVBoxLayout)
from PySide6.QtGui import QAction, QCursor
dictConfig(DIC_LOGGING_CONFIG)
logger = logging.getLogger(conf.LOGGER_NAME)

class TableViewWithContext(QTableView):

    editSig = Signal(int)
    deleteSig = Signal(int)

    def __init__(self, model, parent: PySide6.QtWidgets.QWidget = None) -> None:
        super().__init__(parent)
        self.setModel(model)
        self.setCornerButtonEnabled(False)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
    
    def contextMenuEvent(self, event: PySide6.QtGui.QContextMenuEvent) -> None:
        logger.debug(f"row selected {self.rowAt(event.y())}")
        clickedRow = self.rowAt(event.y())
        if clickedRow == -1:
            self.selectRow(-1)
        else:
            contextMenu = QMenu(self)
            editAction = QAction("Edit", self)
            deleteAction = QAction("Delete", self)
            contextMenu.addActions([editAction, deleteAction])
            contextMenu.popup(QCursor.pos())

            editAction.triggered.connect(lambda: self.editSig.emit(clickedRow))
            deleteAction.triggered.connect(lambda: self.deleteSig.emit(clickedRow))

        return super().contextMenuEvent(event)