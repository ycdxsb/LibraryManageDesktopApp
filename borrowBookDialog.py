import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
import time
from PyQt5.QtSql import *


class borrowBookDialog(QDialog):
    borrow_book_success_signal = pyqtSignal()

    def __init__(self, StudentId, parent=None):
        super(borrowBookDialog, self).__init__(parent)
        self.studentId = StudentId
        self.setUpUI()
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("借阅书籍")

    def setUpUI(self):
        # 书名，书号，作者，分类，添加数量.出版社,出版日期
        # 书籍分类：哲学类、社会科学类、政治类、法律类、军事类、经济类、文化类、教育类、体育类、语言文字类、艺术类、历史类、地理类、天文学类、生物学类、医学卫生类、农业类
        BookCategory = ["哲学", "社会科学", "政治", "法律", "军事", "经济", "文化", "教育", "体育", "语言文字", "艺术", "历史"
            , "地理", "天文学", "生物学", "医学卫生", "农业"]
        self.resize(300, 400)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        # Label控件
        self.borrowStudentLabel = QLabel("借 阅 人:")
        self.borrowStudentIdLabel = QLabel(self.studentId)
        self.titlelabel = QLabel("  借阅书籍")
        self.bookNameLabel = QLabel("书    名:")
        self.bookIdLabel = QLabel("书    号:")
        self.authNameLabel = QLabel("作    者:")
        self.categoryLabel = QLabel("分    类:")
        self.publisherLabel = QLabel("出 版 社:")
        self.publishDateLabel = QLabel("出版日期:")

        # button控件
        self.borrowBookButton = QPushButton("确认借阅")

        # lineEdit控件
        self.bookNameEdit = QLineEdit()
        self.bookIdEdit = QLineEdit()
        self.authNameEdit = QLineEdit()
        self.categoryComboBox = QComboBox()
        self.categoryComboBox.addItems(BookCategory)
        self.publisherEdit = QLineEdit()
        self.publishTime = QLineEdit()

        self.bookNameEdit.setMaxLength(10)
        self.bookIdEdit.setMaxLength(6)
        self.authNameEdit.setMaxLength(10)
        self.publisherEdit.setMaxLength(10)

        # 添加进formlayout
        self.layout.addRow("", self.titlelabel)
        self.layout.addRow(self.borrowStudentLabel, self.borrowStudentIdLabel)
        self.layout.addRow(self.bookNameLabel, self.bookNameEdit)
        self.layout.addRow(self.bookIdLabel, self.bookIdEdit)
        self.layout.addRow(self.authNameLabel, self.authNameEdit)
        self.layout.addRow(self.categoryLabel, self.categoryComboBox)
        self.layout.addRow(self.publisherLabel, self.publisherEdit)
        self.layout.addRow(self.publishDateLabel, self.publishTime)
        self.layout.addRow("", self.borrowBookButton)

        # 设置字体
        font = QFont()
        font.setPixelSize(20)
        self.titlelabel.setFont(font)
        font.setPixelSize(16)
        self.borrowStudentIdLabel.setFont(font)
        font.setPixelSize(14)
        self.borrowStudentLabel.setFont(font)
        self.bookNameLabel.setFont(font)
        self.bookIdLabel.setFont(font)
        self.authNameLabel.setFont(font)
        self.categoryLabel.setFont(font)
        self.publisherLabel.setFont(font)
        self.publishDateLabel.setFont(font)

        self.bookNameEdit.setFont(font)
        self.bookNameEdit.setReadOnly(True)
        self.bookNameEdit.setStyleSheet("background-color:#363636")
        self.bookIdEdit.setFont(font)
        self.authNameEdit.setFont(font)
        self.authNameEdit.setReadOnly(True)
        self.authNameEdit.setStyleSheet("background-color:#363636")
        self.publisherEdit.setFont(font)
        self.publisherEdit.setReadOnly(True)
        self.publisherEdit.setStyleSheet("background-color:#363636")
        self.publishTime.setFont(font)
        self.publishTime.setStyleSheet("background-color:#363636")
        self.categoryComboBox.setFont(font)
        self.categoryComboBox.setStyleSheet("background-color:#363636")

        # button设置
        font.setPixelSize(16)
        self.borrowBookButton.setFont(font)
        self.borrowBookButton.setFixedHeight(32)
        self.borrowBookButton.setFixedWidth(140)

        # 设置间距
        self.titlelabel.setMargin(8)
        self.layout.setVerticalSpacing(10)
        self.borrowBookButton.clicked.connect(self.borrowButtonClicked)
        self.bookIdEdit.textChanged.connect(self.bookIdEditChanged)
        self.bookIdEdit.returnPressed.connect(self.borrowButtonClicked)

    def borrowButtonClicked(self):
        # 获取书号，书号为空或不存在库中，则弹出错误
        # 向Book_User表插入记录，更新User表以及Book表
        BookId = self.bookIdEdit.text()
        # BookId为空的处理
        if (BookId == ""):
            print(QMessageBox.warning(self, "警告", "你所要借的书不存在，请查看输入", QMessageBox.Yes, QMessageBox.Yes))
            return
        # 打开数据库
        db = db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName('./db/LibraryManagement.db')
        db.open()
        query = QSqlQuery()
        # 如果BookId不存在
        sql = "SELECT * FROM Book WHERE BookId='%s'" % BookId
        query.exec_(sql)
        if (not query.next()):
            print(QMessageBox.warning(self, "警告", "你所要借的书不存在，请查看输入", QMessageBox.Yes, QMessageBox.Yes))
            return

        # 借书上限5本
        sql = "SELECT COUNT(StudentId) FROM User_Book WHERE StudentId='%s' AND BorrowState=1" % (
            self.studentId)
        query.exec_(sql)
        if (query.next()):
            borrowNum = query.value(0)
            if (borrowNum == 5):
                QMessageBox.warning(self, "警告", "您借阅的书达到上限（5本）,借书失败！", QMessageBox.Yes, QMessageBox.Yes)
                return
        # 不允许重复借书
        sql = "SELECT COUNT(StudentId) FROM User_Book WHERE  StudentId='%s' AND BookId='%s' AND BorrowState=1" % (
        self.studentId, BookId)
        query.exec_(sql)
        if (query.next() and query.value(0)):
            QMessageBox.warning(self, "警告", "您已经借阅了本书并尚未归还，借阅失败！", QMessageBox.Yes, QMessageBox.Yes)
            return
        # 更新User表
        sql = "UPDATE User SET TimesBorrowed=TimesBorrowed+1,NumBorrowed=NumBorrowed+1 WHERE StudentId='%s'" % self.studentId
        query.exec_(sql)
        db.commit()
        # 更新Book表
        sql = "UPDATE Book SET NumCanBorrow=NumCanBorrow-1,NumBorrowed=NumBorrowed+1 WHERE BookId='%s'" % BookId
        query.exec_(sql)
        db.commit()
        # 插入User_Book表
        timenow = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        sql = "INSERT INTO User_Book VALUES ('%s','%s','%s',NULL,1)" % (self.studentId, BookId, timenow)
        print(sql)
        query.exec_(sql)
        db.commit()
        print(QMessageBox.information(self, "提示", "借阅成功!", QMessageBox.Yes, QMessageBox.Yes))
        self.borrow_book_success_signal.emit()
        self.close()
        return

    def bookIdEditChanged(self):
        bookId = self.bookIdEdit.text()
        if (bookId == ""):
            self.bookNameEdit.clear()
            self.publisherEdit.clear()
            self.authNameEdit.clear()
            self.publishTime.clear()
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName('./db/LibraryManagement.db')
        db.open()
        query = QSqlQuery()
        sql = "SELECT * FROM Book WHERE BookId='%s'" % (bookId)
        query.exec_(sql)
        # 查询对应书号，如果存在就更新form
        if (query.next()):
            self.bookNameEdit.setText(query.value(0))
            self.authNameEdit.setText(query.value(2))
            self.categoryComboBox.setCurrentText(query.value(3))
            self.publisherEdit.setText(query.value(4))
            self.publishTime.setText(query.value(5))
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = borrowBookDialog("PB15000135")
    mainMindow.show()
    sys.exit(app.exec_())
