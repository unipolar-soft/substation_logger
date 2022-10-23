
from PySide6.QtSql import QSqlDatabase, QSqlTableModel
from PySide6.QtCore import Qt

from ..db.db_config import DATABASE_CONNECTION_NAME

class TableModel(QSqlTableModel):
    
    def __init__(self, table, parent= None) -> None:
        database = QSqlDatabase.database(DATABASE_CONNECTION_NAME)
        super().__init__(parent, database)

        self.setTable(table.__tablename__)
        self.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.select()
        columns = [column.info.get('verbose_name') for column in table.__table__.columns]
        
        for index, column in enumerate(columns):
            self.setHeaderData(index, Qt.Horizontal, column)
    