import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
import qdarkstyle
from BookStorageViewer import BookStorageViewer
from borrowBookDialog import borrowBookDialog
from returnBookDialog import returnBookDialog


class StudentHome(QWidget):
    def __init__(self):
        super().__init__()
        self.StudentId = "PB15000135"
        self.resize(900, 600)
        self.setWindowTitle("欢迎使用图书馆管理系统")
        self.setUpUI()

    def setUpUI(self):
        # 总布局
        self.layout = QHBoxLayout(self)
        # 按钮布局
        self.buttonLayout = QVBoxLayout()
        # 按钮
        self.borrowBookButton = QPushButton("借书")
        self.returnBookButton = QPushButton("还书")
        self.myBookStatus = QPushButton("借阅状态")
        self.buttonLayout.addWidget(self.borrowBookButton)
        self.buttonLayout.addWidget(self.returnBookButton)
        self.buttonLayout.addWidget(self.myBookStatus)
        self.borrowBookButton.setFixedWidth(100)
        self.borrowBookButton.setFixedHeight(42)
        self.returnBookButton.setFixedWidth(100)
        self.returnBookButton.setFixedHeight(42)
        self.myBookStatus.setFixedWidth(100)
        self.myBookStatus.setFixedHeight(42)
        font = QFont()
        font.setPixelSize(16)
        self.borrowBookButton.setFont(font)
        self.returnBookButton.setFont(font)
        self.myBookStatus.setFont(font)

        self.storageView = BookStorageViewer()
        self.layout.addLayout(self.buttonLayout)
        self.layout.addWidget(self.storageView)
        self.borrowBookButton.clicked.connect(self.borrowBookButtonClicked)
        self.returnBookButton.clicked.connect(self.returnBookButtonClicked)

    def borrowBookButtonClicked(self):
        borrowDialog = borrowBookDialog(self.StudentId)
        borrowDialog.show()
        borrowDialog.exec_()
        return

    def returnBookButtonClicked(self):
        returnDialog = returnBookDialog(self.StudentId)
        returnDialog.show()
        returnDialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = StudentHome()
    mainMindow.show()
    sys.exit(app.exec_())
