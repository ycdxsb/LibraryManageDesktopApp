import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
import sip
import qdarkstyle
from BookStorageViewer import BookStorageViewer
from borrowBookDialog import borrowBookDialog
from returnBookDialog import returnBookDialog
from BorrowStatusViewer import BorrowStatusViewer


class StudentHome(QWidget):
    def __init__(self, studentId):
        super().__init__()
        self.StudentId = studentId
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
        self.allBookButton = QPushButton("所有书籍")
        self.buttonLayout.addWidget(self.borrowBookButton)
        self.buttonLayout.addWidget(self.returnBookButton)
        self.buttonLayout.addWidget(self.myBookStatus)
        self.buttonLayout.addWidget(self.allBookButton)
        self.borrowBookButton.setFixedWidth(100)
        self.borrowBookButton.setFixedHeight(42)
        self.returnBookButton.setFixedWidth(100)
        self.returnBookButton.setFixedHeight(42)
        self.myBookStatus.setFixedWidth(100)
        self.myBookStatus.setFixedHeight(42)
        self.allBookButton.setFixedWidth(100)
        self.allBookButton.setFixedHeight(42)
        font = QFont()
        font.setPixelSize(16)
        self.borrowBookButton.setFont(font)
        self.returnBookButton.setFont(font)
        self.myBookStatus.setFont(font)
        self.allBookButton.setFont(font)

        self.storageView = BookStorageViewer()
        self.borrowStatusView=BorrowStatusViewer(self.StudentId)
        self.allBookButton.setEnabled(False)

        self.layout.addLayout(self.buttonLayout)
        self.layout.addWidget(self.storageView)
        self.borrowBookButton.clicked.connect(self.borrowBookButtonClicked)
        self.returnBookButton.clicked.connect(self.returnBookButtonClicked)
        self.myBookStatus.clicked.connect(self.myBookStatusClicked)
        self.allBookButton.clicked.connect(self.allBookButtonClicked)

    def borrowBookButtonClicked(self):
        borrowDialog = borrowBookDialog(self.StudentId,self)
        borrowDialog.borrow_book_success_signal.connect(self.borrowStatusView.borrowedQuery)
        borrowDialog.borrow_book_success_signal.connect(self.storageView.searchButtonClicked)
        borrowDialog.show()
        borrowDialog.exec_()
        return

    def returnBookButtonClicked(self):
        returnDialog = returnBookDialog(self.StudentId,self)
        returnDialog.return_book_success_signal.connect(self.borrowStatusView.returnedQuery)
        returnDialog.return_book_success_signal.connect(self.borrowStatusView.borrowedQuery)
        returnDialog.return_book_success_signal.connect(self.storageView.searchButtonClicked)
        returnDialog.show()
        returnDialog.exec_()

    def myBookStatusClicked(self):
        self.layout.removeWidget(self.storageView)
        sip.delete(self.storageView)
        self.storageView = BookStorageViewer()
        self.borrowStatusView = BorrowStatusViewer(self.StudentId)
        self.layout.addWidget(self.borrowStatusView)
        self.allBookButton.setEnabled(True)
        self.myBookStatus.setEnabled(False)
        return

    def allBookButtonClicked(self):
        self.layout.removeWidget(self.borrowStatusView)
        sip.delete(self.borrowStatusView)
        self.borrowStatusView = BorrowStatusViewer(self.StudentId)
        self.storageView = BookStorageViewer()
        self.layout.addWidget(self.storageView)
        self.allBookButton.setEnabled(False)
        self.myBookStatus.setEnabled(True)
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = StudentHome("PB15000135")
    mainMindow.show()
    sys.exit(app.exec_())
