import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
from addBookDialog import addBookDialog
from dropBookDialog import dropBookDialog
from BookStorageViewer import BookStorageViewer


class AdminHome(QWidget):
    def __init__(self):
        super().__init__()
        self.setUpUI()

    def setUpUI(self):
        self.resize(900, 600)
        self.setWindowTitle("欢迎使用图书馆管理系统")
        self.layout = QHBoxLayout()
        self.buttonlayout = QVBoxLayout()
        self.setLayout(self.layout)

        font = QFont()
        font.setPixelSize(16)
        self.storageStatusButton = QPushButton("查看库存")
        self.addBookButton = QPushButton("添加书籍")
        self.dropBookButton = QPushButton("淘汰书籍")
        self.storageStatusButton.setFont(font)
        self.addBookButton.setFont(font)
        self.dropBookButton.setFont(font)
        self.storageStatusButton.setFixedWidth(100)
        self.storageStatusButton.setFixedHeight(42)
        self.addBookButton.setFixedWidth(100)
        self.addBookButton.setFixedHeight(42)
        self.dropBookButton.setFixedWidth(100)
        self.dropBookButton.setFixedHeight(42)
        self.buttonlayout.addWidget(self.addBookButton)
        self.buttonlayout.addWidget(self.dropBookButton)
        self.buttonlayout.addWidget(self.storageStatusButton)
        self.layout.addLayout(self.buttonlayout)
        self.storageView = BookStorageViewer()
        self.layout.addWidget(self.storageView)

        self.addBookButton.clicked.connect(self.addBookButtonClicked)
        self.dropBookButton.clicked.connect(self.dropBookButtonClicked)

    def addBookButtonClicked(self):
        addDialog = addBookDialog()
        addDialog.show()
        addDialog.exec_()

    def dropBookButtonClicked(self):
        dropDialog = dropBookDialog()
        dropDialog.show()
        dropDialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = AdminHome()
    mainMindow.show()
    sys.exit(app.exec_())
