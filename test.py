from PyQt5.QtSql import QSqlDatabase,QSqlQuery

db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName('./db/LibraryManagement.db')
db.open()
query = QSqlQuery()
sql = "SELECT * FROM user WHERE user.StudentId='%s'" % ("0000000000")
query.exec_(sql)
print(query.next())
print(str(query.value(0)))
