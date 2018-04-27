import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
from PyQt5.QtSql import *
import time
import sip

class UserManage(QDialog):
    def __init__(self,parent=None):
        super(UserManage, self).__init__(parent)
        self.resize(280, 400)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setWindowTitle("管理用户")
        # 用户数
        self.userCount = 0
        self.oldDeleteId = ""
        self.oldDeleteName = ""
        self.deleteId = ""
        self.deleteName = ""
        self.setUpUI()

    def setUpUI(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName('./db/LibraryManagement.db')
        self.db.open()
        self.query = QSqlQuery()
        self.getResult()

        # 表格设置
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(self.userCount)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(['学号', '姓名'])
        # 不可编辑
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 标题可拉伸
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 整行选中
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.layout.addWidget(self.tableWidget)
        self.setRows()
        self.deleteUserButton = QPushButton("删 除 用 户")
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.deleteUserButton, Qt.AlignHCenter)
        self.widget = QWidget()
        self.widget.setLayout(hlayout)
        self.widget.setFixedHeight(48)
        font = QFont()
        font.setPixelSize(15)
        self.deleteUserButton.setFixedHeight(36)
        self.deleteUserButton.setFixedWidth(180)
        self.deleteUserButton.setFont(font)
        self.layout.addWidget(self.widget, Qt.AlignCenter)
        # 设置信号
        self.deleteUserButton.clicked.connect(self.deleteUser)
        self.tableWidget.itemClicked.connect(self.getStudentInfo)

    def getResult(self):
        sql = "SELECT StudentId,Name FROM User WHERE IsAdmin=0"
        self.query.exec_(sql)
        self.userCount = 0;
        while (self.query.next()):
            self.userCount += 1;
        sql = "SELECT StudentId,Name FROM User WHERE IsAdmin=0"
        self.query.exec_(sql)

    def setRows(self):
        font = QFont()
        font.setPixelSize(14)
        for i in range(self.userCount):
            if (self.query.next()):
                StudentIdItem = QTableWidgetItem(self.query.value(0))
                StudentNameItem = QTableWidgetItem(self.query.value(1))
                StudentIdItem.setFont(font)
                StudentNameItem.setFont(font)
                StudentIdItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                StudentNameItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget.setItem(i, 0, StudentIdItem)
                self.tableWidget.setItem(i, 1, StudentNameItem)
        return

    def getStudentInfo(self, item):
        row = self.tableWidget.currentIndex().row()
        self.tableWidget.verticalScrollBar().setSliderPosition(row)
        self.getResult()
        i = 0
        while (self.query.next() and i != row):
            i = i + 1
        self.oldDeleteId = self.deleteId
        self.oldDeleteName = self.deleteName
        self.deleteId = self.query.value(0)
        self.deleteName = self.query.value(1)

    def deleteUser(self):
        if (self.deleteId == "" and self.deleteName == ""):
            print(QMessageBox.warning(self, "警告", "请选中要删除的用户", QMessageBox.Yes, QMessageBox.Yes))
            return
        elif (self.deleteId == self.oldDeleteId and self.deleteName == self.oldDeleteName):
            print(QMessageBox.warning(self, "警告", "请选中要删除的用户", QMessageBox.Yes, QMessageBox.Yes))
            return
        if (QMessageBox.information(self, "提醒", "删除用户:%s,%s\n用户一经删除将无法恢复，是否继续?" % (self.deleteId, self.deleteName),
                                    QMessageBox.Yes | QMessageBox.No,
                                    QMessageBox.No) == QMessageBox.No):
            return
        # 从User表删除用户
        sql = "DELETE FROM User WHERE StudentId='%s'" % (self.deleteId)
        self.query.exec_(sql)
        self.db.commit()
        # 归还所有书籍
        sql = "SELECT * FROM User_Book  WHERE StudentId='%s' AND BorrowState=1" % self.deleteId
        self.query.exec_(sql)
        timenow = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        updateQuery=QSqlQuery()
        while (self.query.next()):
            bookId=self.query.value(1)
            sql="UPDATE Book SET NumCanBorrow=NumCanBorrow+1 WHERE BookId='%s'"% bookId
            updateQuery.exec_(sql)
            self.db.commit()
        sql="UPDATE User_Book SET ReturnTime='%s',BorrowState=0 WHERE StudentId='%s' AND BorrowState=1"%(timenow,self.deleteId)
        self.query.exec_(sql)
        self.db.commit()
        print(QMessageBox.information(self,"提醒","删除用户成功!",QMessageBox.Yes,QMessageBox.Yes))
        self.updateUI()
        return

    def updateUI(self):
        self.getResult()
        self.layout.removeWidget(self.widget)
        self.layout.removeWidget(self.tableWidget)
        sip.delete(self.widget)
        sip.delete(self.tableWidget)
        # 表格设置
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(self.userCount)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(['学号', '姓名'])
        # 不可编辑
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 标题可拉伸
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 整行选中
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.layout.addWidget(self.tableWidget)
        self.setRows()
        self.deleteUserButton = QPushButton("删 除 用 户")
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.deleteUserButton, Qt.AlignHCenter)
        self.widget = QWidget()
        self.widget.setLayout(hlayout)
        self.widget.setFixedHeight(48)
        font = QFont()
        font.setPixelSize(15)
        self.deleteUserButton.setFixedHeight(36)
        self.deleteUserButton.setFixedWidth(180)
        self.deleteUserButton.setFont(font)
        self.layout.addWidget(self.widget, Qt.AlignCenter)
        # 设置信号
        self.deleteUserButton.clicked.connect(self.deleteUser)
        self.tableWidget.itemClicked.connect(self.getStudentInfo)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = UserManage()
    mainMindow.show()
    sys.exit(app.exec_())
