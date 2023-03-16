import csv
import os
import sqlite3
import sys

from PIL import Image
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QGridLayout, QLabel, QPushButton, QMessageBox, \
    QFileDialog, QTableWidgetItem
from PyQt5.QtWidgets import QLineEdit, QVBoxLayout, QDateEdit, QPlainTextEdit
from PyQt5.QtCore import Qt
from design import Ui_MainWindow

width = 400
height = 500
file_name_BD = 'data/Contacts.db'


# изменение размера изображения на 140 x 150, создание объекта QPixmap
def image_resize(filename):
    im = Image.open(filename)
    x, y = im.size
    if x > 140 or y > 150:
        im = im.resize((140, 150))
        im.save('picture.png')
        filename = 'picture.png'
    pixmap = QPixmap(filename)
    os.remove('picture.png')
    return pixmap


# создание графического файла из двоичного файла БД
def photo_show(data):
    # создаем файл и сохраняем туда бинарный файл из базы
    fout = open('new.png', 'wb')
    fout.write(data)
    # закрываем созданный файл
    fout.close()
    # созданный файл сжимаем и сохраняем как объект QPixmap
    pixmap = image_resize('new.png')
    # удаляем созданный файл
    os.remove('new.png')
    return pixmap


# проверка номера телефона на корректность
def check_number(number):
    ans = ''
    count_c = 0
    c = 0
    if number[0:2] == '+7':
        number = number[2:]
    elif number[0] == '8':
        number = number[1:]
    for i in range(len(number)):
        # считаем количество цифр в номере
        if number[i] in '0123456789':
            ans += number[i]
        elif number[i] == '-':
            if number[i - 1] == '-':
                return False
        elif number[i] == '(':
            c += 1
            count_c += 1
            if c > 1 or count_c > 2:
                return False
        elif number[i] == ')':
            c -= 1
            count_c += 1
            if c < 0 or count_c > 2:
                return False
        else:
            return False
    if len(ans) == 10:
        return ans
    else:
        return False


# ГЛАВНАЯ ФОРМА
class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.win = QMainWindow()
        self.load_image(file_name_BD)
        self.setGeometry(600, 300, width, height)
        self.con = sqlite3.connect(file_name_BD)
        self.get_list_contacts()
        # добавление нового контакта
        self.btn_add.clicked.connect(self.add_contact)
        # добавление нового контакта
        self.btn_show.clicked.connect(self.show_contact)
        # редактирование данных контакта
        self.btn_del.clicked.connect(self.del_contact)
        # удаление контактов
        self.btn_edit.clicked.connect(self.edit_contact)
        # сортировка по заданному признаку
        self.rb_name.clicked.connect(self.get_list_contacts)
        self.rb_phone.clicked.connect(self.get_list_contacts)
        self.rb_date.clicked.connect(self.get_list_contacts)
        # вывод списка контактов в таблицу csv
        self.save_list.clicked.connect(self.save_csv)

    # проверка наличия файла базы данных
    def load_image(self, name):
        fullname = os.path.join(name)
        if not os.path.isfile(fullname):
            QMessageBox.critical(self, "Ошибка",
                                 f"Файл с базой данных '{fullname}' не найден",
                                 QMessageBox.Ok)
            sys.exit()

    # процедура добавление нового контакта
    def add_contact(self):
        name = ''
        lst = [0, 'Добавление нового контакта', name]
        self.win_add = AddContact(self, lst)
        self.win_add.show()
        self.setEnabled(False)

    # процедура формирования списка выбранных контактов
    def name_choice(self):
        # Получаем номера строк без повторов выделенных ячеек
        rows = list(set([i.row() for i in self.table_list.selectedItems()]))
        # получаем список имен выбранных контактов
        return [self.table_list.item(i, 0).text() for i in rows]

    # процедура вывода информации о контакте
    def show_contact(self):
        name = self.name_choice()
        if len(name) == 0:
            QMessageBox.critical(self, "Сообщение",
                                 "Выберите контакт из списка!", QMessageBox.Ok)
        elif len(name) > 1:
            QMessageBox.critical(self, "Сообщение",
                                 "Выберите только одну запись!", QMessageBox.Ok)
        else:
            self.win_show = ShowContact(self, name)
            self.win_show.show()
            self.setEnabled(False)

    # процедура редактирования данных контакта
    def edit_contact(self):
        name = self.name_choice()
        if len(name) == 0:
            QMessageBox.critical(self, "Сообщение",
                                 "Выберите контакт для редактирования!", QMessageBox.Ok)
        elif len(name) > 1:
            QMessageBox.critical(self, "Сообщение",
                                 "Выберите только одну запись!", QMessageBox.Ok)
        else:
            lst = [1, 'Редактирование данных контакта', name[0]]
            self.win_edit = AddContact(self, lst)
            self.win_edit.show()
            self.setEnabled(False)

    # процедура удаления выбранных контактов
    def del_contact(self):
        name = self.name_choice()
        if len(name) == 0:
            QMessageBox.critical(self, "Сообщение",
                                 "Не выбраны контакты для удаления!", QMessageBox.Ok)
        else:
            # Спрашиваем у пользователя подтверждение на удаление контактов
            valid = QMessageBox.question(
                self, '', "Действительно удалить контакты:\n " + ",\n ".join(name) + '?',
                QMessageBox.Yes, QMessageBox.No)
            # Если пользователь ответил утвердительно, удаляем элементы.
            if valid == QMessageBox.Yes:
                cur = self.con.cursor()
                cur.execute("DELETE FROM contact WHERE name IN (" + ", ".join(
                    '?' * len(name)) + ")", name)
                self.con.commit()
                self.get_list_contacts()

    # процедура вывода списка контактов на QTableWidget
    def get_list_contacts(self):
        cur = self.con.cursor()
        result = cur.execute("SELECT name, number, data "
                             "FROM contact").fetchall()
        if not result:
            QMessageBox.critical(self, "Сообщение",
                                 "Список контактов пуст!", QMessageBox.Ok)
        else:
            if self.rb_name.isChecked():
                result.sort(key=lambda s: str(s[0]))
            if self.rb_phone.isChecked():
                result.sort(key=lambda s: str(s[1]))
            if self.rb_date.isChecked():
                result.sort(key=lambda s: str(s[2]))
            self.table_list.setRowCount(len(result))
            self.table_list.setColumnCount(len(result[0]))
            titles = ['Контакт', 'Телефон', 'Дата рождения']
            # вывод заголовка
            self.table_list.setHorizontalHeaderLabels(titles)
            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    if j == 2 and val == '1900-01-01':
                        self.table_list.setItem(i, j, QTableWidgetItem('не указана'))
                    else:
                        self.table_list.setItem(i, j, QTableWidgetItem(str(val)))
            self.table_list.resizeColumnsToContents()

    # сохранить информацию о контактах в csv-файле (кроме фото)
    def save_csv(self):
        with open('contacts.csv', 'w', newline='') as csvfile:
            writer = csv.writer(
                csvfile, delimiter=';', quotechar='"')
            writer.writerow(['Контакт', 'Телефон', 'email', 'Дата рождения', 'Комментарий'])
            cur = self.con.cursor()
            result = cur.execute("SELECT name, number, email, data, comment "
                                 "FROM contact").fetchall()
            for line in result:
                row = []
                for elem in line:
                    row.append(elem)
                writer.writerow(row)

    def closeEvent(self, event):
        self.con.close()


# создает окно, для вывода информации о выбранном контакте
class ShowContact(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.name = args[-1][0]
        self.con = sqlite3.connect(file_name_BD)

        self.data = self.row_data(self.name)
        self.setGeometry(1000, 300, width, height)
        self.setWindowTitle('Данные о контакте')
        self.setFixedSize(width, height)
        self.initUI()

    def initUI(self):
        font = QFont()
        font.setPointSize(12)
        self.setFont(font)

        font_titul = QFont()
        font_titul.setPointSize(14)
        font_titul.setBold(True)
        titul = QLabel()
        titul.setFixedWidth(width)
        titul.setAlignment(Qt.AlignCenter)
        titul.setText(self.name)
        titul.setFont(font_titul)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(titul)

        self.photo_view = QLabel()
        self.photo_view.setFixedWidth(width)
        self.photo_view.setAlignment(Qt.AlignCenter)
        self.photo_view.adjustSize()
        # выводим на метку загруженную картинку
        self.photo_view.setPixmap(photo_show(self.data[4]))
        self.vbox.addWidget(self.photo_view)
        self.vbox.addWidget(QLabel('телефон: ' + str(self.data[1])))
        self.vbox.addWidget(QLabel('email: ' + self.data[2]))
        self.vbox.addWidget(QLabel('дата рождения: ' + self.data[3]))
        self.comment = QPlainTextEdit()
        self.comment.setPlainText(self.data[5])
        self.comment.setEnabled(False)
        self.vbox.addWidget(self.comment)
        self.setLayout(self.vbox)
        self.vbox.addStretch(1)

    def row_data(self, name_contact):
        cur = self.con.cursor()
        sql = f"SELECT * FROM contact WHERE name = '{name_contact}'"
        result = cur.execute(sql).fetchone()
        return result

    def closeEvent(self, event):
        self.con.close()
        ex.setEnabled(True)


# создает окно, для добавления нового контакта,
# или редактирования информации об имеющемся контакте
class AddContact(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.args = args[-1]
        self.key = self.args[0]
        self.name = ''
        self.phone = ''
        self.email = ''
        self.date = sqlite3.Date(1900, 1, 1)
        self.filename = 'data/photo_fon.png'
        self.comment = ''
        self.con = sqlite3.connect(file_name_BD)
        self.read_contact()
        self.initUI(args)
        # процедура сохранения данных контакта
        self.btn_add.clicked.connect(self.save_contact)
        # процедура выбора фото для аватарки
        self.photo_add.clicked.connect(self.add_photo)

    # сведения из БД для заполнения формы
    def read_contact(self):
        if self.key:
            self.name = self.args[2]
            cur = self.con.cursor()
            sql = f"SELECT * FROM contact WHERE name = '{self.name}'"
            self.data = cur.execute(sql).fetchone()
            self.phone = str(self.data[1])
            self.email = self.data[2]
            y, m, d = map(int, self.data[3].split('-'))
            self.date = sqlite3.Date(y, m, d)

    # создание окна для редактирования и ввода данных контакта
    def initUI(self, args):
        self.setGeometry(1000, 300, width, height)
        self.setWindowTitle(args[-1][1])
        self.setFixedSize(width, height)
        font = QFont()
        font.setPointSize(10)
        self.setFont(font)

        font_titul = QFont()
        font_titul.setPointSize(14)
        font_titul.setBold(True)
        titul = QLabel()
        titul.setText('Сведения о контакте:')
        titul.setFont(font_titul)

        self.layout_tab = QGridLayout()
        self.layout_tab.setSpacing(10)
        self.layout_tab.addWidget(titul, 0, 0, 1, 2)

        # заполнение левой колонки
        label_name = 'Имя'
        label_phone = 'телефон в формате:'
        if self.key == 0:
            label_name = '*' + label_name
            label_phone = '*' + label_phone
        self.layout_tab.addWidget(QLabel(label_name), 1, 0)
        self.layout_tab.addWidget(QLabel(label_phone), 2, 0)
        self.layout_tab.addWidget(QLabel('9123456789 (10 знаков)'), 3, 0)
        self.layout_tab.addWidget(QLabel('дата рождения'), 4, 0)
        self.layout_tab.addWidget(QLabel('email'), 5, 0)
        self.photo_add = QPushButton()
        self.photo_add.setText('Добавить фото')
        self.layout_tab.addWidget(self.photo_add, 6, 0)
        self.layout_tab.addWidget(QLabel('Размер 140 x 150 px'), 7, 0)
        self.photo = QLabel()
        self.photo.setFixedSize(140, 150)
        if self.key:
            self.photo.setPixmap(photo_show(self.data[4]))
        else:
            self.read_photo_standart()
        self.layout_tab.addWidget(self.photo, 8, 0)
        self.btn_add = QPushButton()
        self.btn_add.setText('Сохранить данные контакта')
        self.layout_tab.addWidget(self.btn_add, 9, 0, 1, 2)
        self.layout_tab.addWidget(QLabel('* отмечены поля, обязательные '
                                         'для заполнения'), 10, 0, 1, 2)

        # заполнение правой колонки
        self.name_edit = QLineEdit(self.name)
        self.layout_tab.addWidget(self.name_edit, 1, 1)
        self.phone_edit = QLineEdit(self.phone)
        self.layout_tab.addWidget(self.phone_edit, 2, 1, 2, 1)
        self.data_edit = QDateEdit()
        # установка начального значения даты и её формата
        self.data_edit.setDate(self.date)
        # внешний вид отображения даты
        self.data_edit.setDisplayFormat("yyyy-MM-dd")
        self.data_edit.setFixedSize(100, 20)
        self.layout_tab.addWidget(self.data_edit, 4, 1)
        self.email_edit = QLineEdit(self.email)
        self.layout_tab.addWidget(self.email_edit, 5, 1)
        self.layout_tab.addWidget(QLabel('Комментарий'), 6, 1)
        self.comment_edit = QPlainTextEdit()
        self.layout_tab.addWidget(self.comment_edit, 7, 1, 2, 1)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.layout_tab)
        self.setLayout(self.vbox)
        self.vbox.addStretch(1)

    # чтение файла аватарки по умолчанию из текущей директории для вывода на метку
    def read_photo_standart(self):
        # проверяем, есть ли файл для аватарки в директории,
        # если нет, предлагается его выбрать в обязательном порядке
        fullname = os.path.join(self.filename)
        if not os.path.isfile(fullname):
            QMessageBox.critical(self, "Ошибка",
                                 f"В директории нет файла аватарки '{fullname}' \n"
                                 f" выберите подходящий файл!",
                                 QMessageBox.Ok)
            self.filename = ''
            while self.filename == '':
                self.add_photo()
        else:
            self.photo.setPixmap(QPixmap(self.filename))

    # поиск совпадающего контакта по фамилии
    def search_contact_fio(self, fio_contact):
        cur = self.con.cursor()
        sql = f"SELECT * FROM contact WHERE name = '{fio_contact}'"
        result = cur.execute(sql).fetchall()
        if not result:
            return False
        else:
            return result

    # поиск совпадающего контакта по телефону
    def search_contact_phone(self, phone_contact):
        cur = self.con.cursor()
        sql = f"SELECT name FROM contact WHERE number = '{phone_contact}'"
        result = cur.execute(sql).fetchall()
        if not result:
            return False
        else:
            return result

    # сохранение данных формы
    def save_contact(self):
        if not(self.name_edit.text()):
            QMessageBox.critical(self, 'Ошибка!',
                                 "Введите имя контакта!",
                                 QMessageBox.Ok)
        elif self.key == 0 and self.search_contact_fio(self.name_edit.text()):
            QMessageBox.critical(self, "Ошибка!",
                                 "Контакт уже есть в списке!",
                                 QMessageBox.Ok)
        elif self.phone_edit.text() == '':
            QMessageBox.critical(self, 'Ошибка!',
                                 "Введите номер телефона!",
                                 QMessageBox.Ok)
        else:
            number = ''.join(self.phone_edit.text().split())
            if not check_number(number):
                QMessageBox.critical(self, "Ошибка!",
                                     "Неверный формат номера телефона",
                                     QMessageBox.Ok)
            else:
                self.phone_edit.setText(check_number(number))
                result = self.search_contact_phone(self.phone_edit.text())
                if self.key == 0 and result:
                    result = str(result[0][0])
                    QMessageBox.critical(self, "Ошибка!",
                                         f"Такой телефон уже есть у\n {result}",
                                         QMessageBox.Ok)
                else:
                    cur = self.con.cursor()
                    # преобразование аватарки в бинарный файл
                    fin = open(self.filename, "rb")
                    img = fin.read()
                    fin.close()
                    binary = sqlite3.Binary(img)
                    if self.key:
                        # запрос на замену данных контакта
                        cur.execute("""UPDATE contact 
                                    SET name=?, number=?, email=?, data=?, photo=?, comment=?
                                    WHERE name=?""",
                                    (self.name_edit.text(),
                                     self.phone_edit.text(),
                                     self.email_edit.text(),
                                     self.data_edit.date().toString('yyyy-MM-dd'),
                                     binary,
                                     self.comment_edit.toPlainText(),
                                     self.name))
                    else:
                        # запрос на добавление нового контакта в БД
                        cur.execute("INSERT INTO contact"
                                    "(name, number, email, data, photo, comment)"
                                    "VALUES(?, ?, ?, ?, ?, ?)",
                                    (self.name_edit.text(),
                                     self.phone_edit.text(),
                                     self.email_edit.text(),
                                     self.data_edit.date().toString('yyyy-MM-dd'),
                                     binary,
                                     self.comment_edit.toPlainText()))
                    self.con.commit()
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setWindowTitle("Информация")
                    msg.setInformativeText(f"Данные контакта {self.name_edit.text()} сохранены!")
                    msg.exec()
                    if self.key:
                        valid = QMessageBox.question(
                            self, '', 'Закончить редактирование?',
                            QMessageBox.Yes, QMessageBox.No)
                        if valid == QMessageBox.Yes:
                            self.close()
                        else:
                            self.name = self.name_edit.text()
                    else:
                        valid = QMessageBox.question(
                            self, '', 'Добавить ещё контакт?',
                            QMessageBox.Yes, QMessageBox.No)
                        if valid == QMessageBox.No:
                            self.close()
                        else:
                            self.clear_data()

    # очистка данных формы
    def clear_data(self):
        self.filename = 'data/photo_fon.png'
        self.read_photo_standart()
        self.phone_edit.setText('')
        self.email_edit.setText('')
        self.comment_edit.setPlainText('')
        self.name_edit.setText('')

    # выбор графического файла для аватарки
    def add_photo(self):
        self.filename = QFileDialog.getOpenFileName(self,
                                                    'Выберите фото', '',
                                                    'Картинки (*.png)')[0]
        if self.filename != '':
            self.photo.setPixmap(image_resize(self.filename))

    def closeEvent(self, event):
        self.con.close()
        ex.setEnabled(True)
        ex.get_list_contacts()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
