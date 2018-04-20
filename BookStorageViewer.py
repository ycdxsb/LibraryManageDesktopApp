import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
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
        self.tableViewer = None
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
        self.pageLabel = QLabel("页")
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

        # tableViewer
        # 序号，书名，书号，作者，分类，出版社，出版时间，库存，剩余可借
        self.tableViewer = QTableView()
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName('./db/LibraryManagement.db')
        self.db.open()
        self.model = QSqlTableModel()
        self.model.setTable("book")
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.setFilter("BookId LIKE 'I%'")
        self.model.select()
        self.model.setHeaderData(0, Qt.Horizontal, "书名")
        self.model.setHeaderData(1, Qt.Horizontal, "书号")
        self.model.setHeaderData(2, Qt.Horizontal, "作者")
        self.model.setHeaderData(3, Qt.Horizontal, "分类")
        self.model.setHeaderData(4, Qt.Horizontal, "出版社")
        self.model.setHeaderData(5, Qt.Horizontal, "出版时间")
        self.model.setHeaderData(6, Qt.Horizontal, "库存")
        self.model.setHeaderData(7, Qt.Horizontal, "剩余可借")
        self.model.setHeaderData(8, Qt.Horizontal, "已借")
        self.tableViewer.setModel(self.model)
        self.tableViewer.horizontalHeader().setStretchLastSection(True)
        self.tableViewer.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableViewer.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.layout.addLayout(self.Hlayout1)
        self.layout.addWidget(self.tableViewer)
        self.layout.addLayout(self.Hlayout2)
        self.setLayout(self.layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = BookStorageViewer()
    mainMindow.show()
    sys.exit(app.exec_())
