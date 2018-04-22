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
        self.returnedTableView = QTableView()

        self.layout.addWidget(self.borrowedLabel)
        self.layout.addWidget(self.returnedLabel)
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = BorrowStatusViewer("PB15000135")
    mainMindow.show()
    sys.exit(app.exec_())
