import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("pr1.ui.", self)
        self.con = sqlite3.connect("films_db.sqlite")
        self.pushButton.clicked.connect(self.start)
        self.pushButton_2.clicked.connect(self.change)
        self.titles = None

    def start(self):
        cur = self.con.cursor()
        self.item_id = self.spinBox.text()
        self.result = cur.execute("SELECT * FROM films WHERE id=?",
                                  (self.item_id,)).fetchall()
        self.tableWidget.setRowCount(len(self.result))
        if not self.result:
            return
        self.tableWidget.setColumnCount(len(self.result[0]))
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(self.result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def change(self):
        valid = QMessageBox.question(
            self, '', "Действительно заменить элементы с id " + self.item_id,
            QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            cur = self.con.cursor()
            cur.execute(f"""UPDATE films
    SET title = '{self.result[0][1][::-1]}', year = year + 1000, duration = duration * 2
    WHERE title = '{self.result[0][1]}'""")
            self.con.commit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())