# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import qdarkstyle
from PyQt5.QtSql import *


class BookStorageViewer(QWidget):
    def __init__(self):
        super(BookStorageViewer, self).__init__()
        self.resize(700, 500)
        self.setWindowTitle("欢迎使用图书馆管理系统")
        # 查询模型
        self.queryModel = None
        # 数据表
        self.tableView = None
        # 当前页
        self.currentPage = 0
        # 总页数
        self.totalPage = 0
        # 总记录数
        self.totalRecord = 0
        # 每页数据数
        self.pageRecord = 5
        self.setUpUI()

    def setUpUI(self):
        self.layout = QVBoxLayout()
        self.Hlayout1 = QHBoxLayout()
        self.Hlayout2 = QHBoxLayout()

        # Hlayout1控件的初始化
        self.searchEdit = QLineEdit()
        self.searchEdit.setFixedHeight(32)
        font = QFont()
        font.setPixelSize(15)
        self.searchEdit.setFont(font)

        self.searchButton = QPushButton("查询")
        self.searchButton.setFixedHeight(32)
        self.searchButton.setFont(font)
        self.searchButton.setIcon(QIcon(QPixmap("./images/search.png")))

        self.condisionComboBox = QComboBox()
        searchCondision = ['按书名查询', '按书号查询', '按作者查询', '按分类查询', '按出版社查询']
        self.condisionComboBox.setFixedHeight(32)
        self.condisionComboBox.setFont(font)
        self.condisionComboBox.addItems(searchCondision)

        self.Hlayout1.addWidget(self.searchEdit)
        self.Hlayout1.addWidget(self.searchButton)
        self.Hlayout1.addWidget(self.condisionComboBox)

        # Hlayout2初始化
        self.jumpToLabel = QLabel("跳转到第")
        self.pageEdit = QLineEdit()
        self.pageEdit.setFixedWidth(30)
        s = "/" + str(self.totalPage) + "页"
        self.pageLabel = QLabel(s)
        self.jumpToButton = QPushButton("跳转")
        self.prevButton = QPushButton("前一页")
        self.prevButton.setFixedWidth(60)
        self.backButton = QPushButton("后一页")
        self.backButton.setFixedWidth(60)

        Hlayout = QHBoxLayout()
        Hlayout.addWidget(self.jumpToLabel)
        Hlayout.addWidget(self.pageEdit)
        Hlayout.addWidget(self.pageLabel)
        Hlayout.addWidget(self.jumpToButton)
        Hlayout.addWidget(self.prevButton)
        Hlayout.addWidget(self.backButton)
        widget = QWidget()
        widget.setLayout(Hlayout)
        widget.setFixedWidth(300)
        self.Hlayout2.addWidget(widget)

        # tableView
        # 序号，书名，书号，作者，分类，出版社，出版时间，库存，剩余可借
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('./db/LibraryManagement.db')
        self.db.open()
        self.tableView = QTableView()
        self.queryModel = QSqlQueryModel(self)
        self.searchButtonClicked()
        self.tableView.setModel(self.queryModel)

        print(self.queryModel.setHeaderData(0, Qt.Horizontal, "书名"))
        self.queryModel.setHeaderData(1, Qt.Horizontal, "书号")
        self.queryModel.setHeaderData(2, Qt.Horizontal, "作者")
        self.queryModel.setHeaderData(3, Qt.Horizontal, "分类")
        self.queryModel.setHeaderData(4, Qt.Horizontal, "出版社")
        self.queryModel.setHeaderData(5, Qt.Horizontal, "出版时间")
        self.queryModel.setHeaderData(6, Qt.Horizontal, "库存")
        self.queryModel.setHeaderData(7, Qt.Horizontal, "剩余可借")
        self.queryModel.setHeaderData(8, Qt.Horizontal, "已借")

        self.layout.addLayout(self.Hlayout1)
        self.layout.addWidget(self.tableView)
        self.layout.addLayout(self.Hlayout2)
        self.setLayout(self.layout)
        self.searchButtonClicked()
        self.searchButton.clicked.connect(self.searchButtonClicked)
        self.prevButton.clicked.connect(self.prevButtonClicked)
        self.backButton.clicked.connect(self.backButtonClicked)
        self.jumpToButton.clicked.connect(self.jumpToButtonClicked)

    # 得到记录数
    def getTotalRecordCount(self):
        self.queryModel.setQuery("SELECT * FROM Book")
        self.totalRecord = self.queryModel.rowCount()
        return

    # 得到总页数
    def getPageCount(self):
        self.getTotalRecordCount()
        # 上取整
        self.totalPage = int((self.totalRecord + self.pageRecord - 1) / self.pageRecord)
        return

    # 分页记录查询
    def recordQuery(self, index):
        queryCondition = ""
        if (self.searchEdit.text() == ""):
            queryCondition = ("select * from Book limit %d,%d " % (index, self.pageRecord))
            self.queryModel.setQuery(queryCondition)
            print(queryCondition)
            return
        conditionChoice = self.condisionComboBox.currentText()
        if (conditionChoice == "按书名查询"):
            conditionChoice = 'BookName'
        elif (conditionChoice == "按书号查询"):
            conditionChoice = 'BookId'
        elif (conditionChoice == "按作者查询"):
            conditionChoice = 'Auth'
        elif (conditionChoice == '按分类查询'):
            conditionChoice = 'Category'
        else:
            conditionChoice = 'publisher'
        # 得到模糊查询条件
        temp = self.searchEdit.text()
        s = '%'
        for i in range(0, len(temp)):
            s = s + temp[i] + "%"
        queryCondition = ("SELECT * FROM Book WHERE %s LIKE '%s' LIMIT %d,%d " % (
            conditionChoice, s, index, self.pageRecord))
        print(queryCondition)
        self.queryModel.setQuery(queryCondition)
        return

    # 点击查询
    def searchButtonClicked(self):
        self.currentPage = 1
        self.pageEdit.setText(str(self.currentPage))
        self.getPageCount()
        s = "/" + str(int(self.totalPage)) + "页"
        self.pageLabel.setText(s)
        index = (self.currentPage - 1) * self.pageRecord
        self.recordQuery(index)
        return

    # 向前翻页
    def prevButtonClicked(self):
        self.currentPage -= 1
        if (self.currentPage <= 1):
            self.currentPage = 1
        self.pageEdit.setText(str(self.currentPage))
        index = (self.currentPage - 1) * self.pageRecord
        self.recordQuery(index)
        return

    # 向后翻页
    def backButtonClicked(self):
        self.currentPage += 1
        if (self.currentPage >= int(self.totalPage)):
            self.currentPage = int(self.totalPage)
        self.pageEdit.setText(str(self.currentPage))
        index = (self.currentPage - 1) * self.pageRecord
        self.recordQuery(index)
        return

    # 点击跳转
    def jumpToButtonClicked(self):
        self.currentPage = int(self.pageEdit.text())
        index = (self.currentPage - 1) * self.pageRecord
        self.recordQuery(index)
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = BookStorageViewer()
    mainMindow.show()
    sys.exit(app.exec_())
