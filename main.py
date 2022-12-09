import requests
from bs4 import BeautifulSoup
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem
import sys
from pyqt5_plugins.examplebuttonplugin import QtGui

answer = ['']


class Form1(QtWidgets.QMainWindow):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        super(Form1, self).__init__()
        uic.loadUi('UI/firstactivity.ui', self)
        self.getData.clicked.connect(self.find_book)
        self.setWindowIcon(QtGui.QIcon('icon.png'))

    def find_book(self):
        if self.Bookname.text() == "":
            self.label.setStyleSheet("color: rgb(255,0,0,1); font-size:22px;")
            self.label.setText("Введите название книги")
        else:
            try:
                bookName = self.Bookname.text()
                link = "https://knigogo.net/?s=" + bookName
                responce = requests.get(link)
                src = responce.text


                with open("answer.html", "w", encoding="utf-8") as file:
                    file.write(src)
                answer[0] = self.Bookname.text()
                self.switch_window.emit('1>2')

            except:
                self.label.setText("Ошибка подключения")




class Form2(QtWidgets.QMainWindow):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        super(Form2, self).__init__()
        uic.loadUi('UI/secondactivity.ui', self)
        self.setWindowTitle('Список книг')
        self.Back.clicked.connect(self.back)
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        parsing(self)

    def back(self):
        self.switch_window.emit('1<2')

def parsing(self):
    link = "https://knigogo.net/?s=" + answer[0]
    responce = requests.get(link)
    src = responce.text
    soup = BeautifulSoup(src, "lxml")


    self.Label.setText("Поиск книг по:")
    self.Search.setText(answer[0])

    book_title = soup.find_all(class_="book_name")
    self.tableWidget.setRowCount(len(book_title))


    author = soup.find_all(class_="pisatel-thrumbnail")
    url=[]

    for a in soup.find_all('a', class_="book_link"):
        url.append(a.get('href'))




    for row in range(self.tableWidget.rowCount()):
        self.tableWidget.setItem(row, 0, QTableWidgetItem(book_title[row].text.replace('\n', '')))
        self.tableWidget.setItem(row, 1, QTableWidgetItem(author[row].text.replace('\n', '')))
        self.tableWidget.setItem(row, 2, QTableWidgetItem(url[row]))



def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Form1()
    window.show()
    sys.exit(app.exec_())


class Controller:
    def __init__(self):
        pass

    def select_forms(self, text):
        if text == '1':
            self.form1 = Form1()
            self.form1.switch_window.connect(self.select_forms)
            self.form1.show()
        if text == '1>2':
            self.form2 = Form2()
            self.form2.switch_window.connect(self.select_forms)
            self.form2.show()
            self.form1.close()
        if text == '1<2':
            self.form1 = Form1()
            self.form1.switch_window.connect(self.select_forms)
            self.form1.show()
            self.form2.close()




def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.select_forms("1")
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
