import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
from PyQt5.QtSql import *
import time


class dropBookDialog(QDialog):
    drop_book_successful_signal=pyqtSignal()

    def __init__(self, parent=None):
        super(dropBookDialog, self).__init__(parent)
        self.setUpUI()
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("删除书籍")

    def setUpUI(self):
        # 书名，书号，作者，分类，添加数量.出版社,出版日期
        # 书籍分类：哲学类、社会科学类、政治类、法律类、军事类、经济类、文化类、教育类、体育类、语言文字类、艺术类、历史类、地理类、天文学类、生物学类、医学卫生类、农业类
        BookCategory = ["哲学", "社会科学", "政治", "法律", "军事", "经济", "文化", "教育", "体育", "语言文字", "艺术", "历史"
            , "地理", "天文学", "生物学", "医学卫生", "农业"]
        self.resize(300, 400)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        # Label控件
        self.titlelabel = QLabel("  淘汰书籍")
        self.bookNameLabel = QLabel("书    名:")
        self.bookIdLabel = QLabel("书    号:")
        self.authNameLabel = QLabel("作    者:")
        self.categoryLabel = QLabel("分    类:")
        self.publisherLabel = QLabel("出 版 社:")
        self.publishDateLabel = QLabel("出版日期:")
        self.dropNumLabel = QLabel("数    量:")

        # button控件
        self.dropBookButton = QPushButton("淘 汰")

        # lineEdit控件
        self.bookNameEdit = QLineEdit()
        self.bookIdEdit = QLineEdit()
        self.authNameEdit = QLineEdit()
        self.categoryComboBox = QComboBox()
        self.categoryComboBox.addItems(BookCategory)
        self.publisherEdit = QLineEdit()
        self.publishTime = QLineEdit()
        # self.publishDateEdit = QLineEdit()
        self.dropNumEdit = QLineEdit()

        self.bookNameEdit.setMaxLength(10)
        self.bookIdEdit.setMaxLength(6)
        self.authNameEdit.setMaxLength(10)
        self.publisherEdit.setMaxLength(10)
        self.dropNumEdit.setMaxLength(12)
        self.dropNumEdit.setValidator(QIntValidator())

        # 添加进formlayout
        self.layout.addRow("", self.titlelabel)
        self.layout.addRow(self.bookNameLabel, self.bookNameEdit)
        self.layout.addRow(self.bookIdLabel, self.bookIdEdit)
        self.layout.addRow(self.authNameLabel, self.authNameEdit)
        self.layout.addRow(self.categoryLabel, self.categoryComboBox)
        self.layout.addRow(self.publisherLabel, self.publisherEdit)
        self.layout.addRow(self.publishDateLabel, self.publishTime)
        self.layout.addRow(self.dropNumLabel, self.dropNumEdit)
        self.layout.addRow("", self.dropBookButton)

        # 设置字体
        font = QFont()
        font.setPixelSize(20)
        self.titlelabel.setFont(font)
        font.setPixelSize(14)
        self.bookNameLabel.setFont(font)
        self.bookIdLabel.setFont(font)
        self.authNameLabel.setFont(font)
        self.categoryLabel.setFont(font)
        self.publisherLabel.setFont(font)
        self.publishDateLabel.setFont(font)
        self.dropNumLabel.setFont(font)

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
        self.dropNumEdit.setFont(font)

        # button设置
        font.setPixelSize(16)
        self.dropBookButton.setFont(font)
        self.dropBookButton.setFixedHeight(32)
        self.dropBookButton.setFixedWidth(140)

        # 设置间距
        self.titlelabel.setMargin(8)
        self.layout.setVerticalSpacing(10)

        self.dropBookButton.clicked.connect(self.dropBookButtonClicked)
        self.bookIdEdit.textChanged.connect(self.bookIdEditChanged)

    def bookIdEditChanged(self):
        bookId = self.bookIdEdit.text()
        if (bookId == ""):
            self.bookNameEdit.clear()
            self.publisherEdit.clear()
            self.authNameEdit.clear()
            self.dropNumEdit.clear()
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

    def dropBookButtonClicked(self):
        bookId = self.bookIdEdit.text()
        dropNum = 0
        if (self.dropNumEdit.text() == ""):
            print(QMessageBox.warning(self, "警告", "淘汰数目为空，请检查输入，操作失败"), QMessageBox.Yes, QMessageBox.Yes)
            return
        dropNum = int(self.dropNumEdit.text())
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName('./db/LibraryManagement.db')
        db.open()
        query = QSqlQuery()
        sql = "SELECT * FROM Book WHERE BookId='%s'" % (bookId)
        query.exec_(sql)
        if (query.next()):
            if (dropNum > query.value(7) or dropNum < 0):
                print(QMessageBox.warning(self, "警告", "最多可淘汰%d本，请检查输入" % (query.value(7)), QMessageBox.Yes,
                                          QMessageBox.Yes))
                return
        # 更新Book表和BuyorDrop表
        # 如果drop书目和当前库存相同，则直接删除Book记录（这里先默认当前所有书都在库存中）
        if (dropNum == query.value(6)):
            sql = "DELETE  FROM Book WHERE BookId='%s'" % (bookId)
        else:
            sql = "UPDATE BOOK SET NumStorage=NumStorage-%d,NumCanBorrow=NumCanBorrow-%d WHERE BookId='%s'" % (
                dropNum, dropNum, bookId)
        query.exec_(sql)
        db.commit()

        timenow = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        sql = "INSERT INTO buyordrop VALUES ('%s','%s',0,%d)" % (bookId, timenow, dropNum)
        query.exec_(sql)
        db.commit()
        print(QMessageBox.information(self, "提示", "淘汰书籍成功!", QMessageBox.Yes, QMessageBox.Yes))
        self.drop_book_successful_signal.emit()
        self.close()
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = dropBookDialog()
    mainMindow.show()
    sys.exit(app.exec_())
