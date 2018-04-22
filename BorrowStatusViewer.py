import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import qdarkstyle
from PyQt5.QtSql import *


class BorrowStatusViewer(QWidget):
    def __init__(self, studentId):
        super(BorrowStatusViewer, self).__init__()
        self.resize(700, 500)
        self.studentId = studentId
        self.setWindowTitle("欢迎使用图书馆管理系统")
        self.setUpUI()

    def setUpUI(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName('./db/LibraryManagement.db')
        self.db.open()
        # 分为两块，上方是已借未归还书，下方是已归还书
        self.layout = QVBoxLayout(self)
        # Label设置
        self.borrowedLabel = QLabel("未归还:")
        self.returnedLabel = QLabel("已归还:")
        self.borrowedLabel.setFixedHeight(32)
        self.borrowedLabel.setFixedWidth(60)
        self.returnedLabel.setFixedHeight(32)
        self.returnedLabel.setFixedWidth(60)
        font = QFont()
        font.setPixelSize(18)
        self.borrowedLabel.setFont(font)
        self.returnedLabel.setFont(font)

        # Table和Model
        self.borrowedTableView = QTableView()
        self.borrowedTableView.horizontalHeader().setStretchLastSection(True)
        self.borrowedTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.borrowedTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.returnedTableView = QTableView()
        self.returnedTableView.horizontalHeader().setStretchLastSection(True)
        self.returnedTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.returnedTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.borrowedQueryModel = QSqlQueryModel()
        self.returnedQueryModel = QSqlQueryModel()
        self.borrowedTableView.setModel(self.borrowedQueryModel)
        self.returnedTableView.setModel(self.returnedQueryModel)
        self.borrowedQuery()
        self.borrowedQueryModel.setHeaderData(0, Qt.Horizontal, "书名")
        self.borrowedQueryModel.setHeaderData(1, Qt.Horizontal, "书号")
        self.borrowedQueryModel.setHeaderData(2, Qt.Horizontal, "作者")
        self.borrowedQueryModel.setHeaderData(3, Qt.Horizontal, "分类")
        self.borrowedQueryModel.setHeaderData(4, Qt.Horizontal, "出版社")
        self.borrowedQueryModel.setHeaderData(5, Qt.Horizontal, "出版时间")
        self.borrowedQueryModel.setHeaderData(6, Qt.Horizontal, "借出时间")

        self.returnedQuery()
        self.returnedQueryModel.setHeaderData(0, Qt.Horizontal, "书名")
        self.returnedQueryModel.setHeaderData(1, Qt.Horizontal, "书号")
        self.returnedQueryModel.setHeaderData(2, Qt.Horizontal, "作者")
        self.returnedQueryModel.setHeaderData(3, Qt.Horizontal, "分类")
        self.returnedQueryModel.setHeaderData(4, Qt.Horizontal, "出版社")
        self.returnedQueryModel.setHeaderData(5, Qt.Horizontal, "出版时间")
        self.returnedQueryModel.setHeaderData(6, Qt.Horizontal, "借阅时间")
        self.returnedQueryModel.setHeaderData(7, Qt.Horizontal, "归还时间")

        self.layout.addWidget(self.borrowedLabel)
        self.layout.addWidget(self.borrowedTableView)
        self.layout.addWidget(self.returnedLabel)
        self.layout.addWidget(self.returnedTableView)
        return

    def borrowedQuery(self):
        sql = "SELECT Book.BookName,Book.BookId,Auth,Category,Publisher,PublishTime,BorrowTime  FROM Book,User_Book WHERE Book.BookId=User_Book.BookId AND User_Book.BorrowState=1 AND StudentId='%s'" % self.studentId
        self.borrowedQueryModel.setQuery(sql)
        return

    def returnedQuery(self):
        sql = "SELECT Book.BookName,Book.BookId,Auth,Category,Publisher,PublishTime,BorrowTime,ReturnTime  FROM Book,User_Book WHERE Book.BookId=User_Book.BookId AND User_Book.BorrowState=0 AND StudentId='%s'" % self.studentId
        self.returnedQueryModel.setQuery(sql)
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = BorrowStatusViewer("PB15000135")
    mainMindow.show()
    sys.exit(app.exec_())
