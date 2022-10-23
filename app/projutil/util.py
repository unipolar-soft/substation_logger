from sqlalchemy.orm import Session
from PySide6.QtWidgets import QWidget, QMessageBox, QErrorMessage
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter, QIntValidator,
    QPalette, QPixmap, QRadialGradient, QTransform, QAction)

from .conf import APP_TITLE

def show_message(text):
    msg = QMessageBox()
    msg.setWindowTitle(APP_TITLE)
    # msg.setWindowIcon(QIcon(QPixmap(":/icons/p16.png")))
    msg.setText(text)
    msg.exec()

if __name__=="__main__":
    pass