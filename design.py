# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'contacts.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 500)
        MainWindow.setMinimumSize(QtCore.QSize(400, 500))
        MainWindow.setMaximumSize(QtCore.QSize(400, 500))
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 381, 451))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.table_list = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        self.table_list.setObjectName("table_list")
        self.table_list.setColumnCount(0)
        self.table_list.setRowCount(0)
        self.verticalLayout.addWidget(self.table_list)
        self.groupBox = QtWidgets.QGroupBox(self.verticalLayoutWidget)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 80))
        self.groupBox.setObjectName("groupBox")
        self.rb_name = QtWidgets.QRadioButton(self.groupBox)
        self.rb_name.setGeometry(QtCore.QRect(10, 20, 150, 17))
        self.rb_name.setMinimumSize(QtCore.QSize(150, 0))
        self.rb_name.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.rb_name.setChecked(True)
        self.rb_name.setObjectName("rb_name")
        self.rb_phone = QtWidgets.QRadioButton(self.groupBox)
        self.rb_phone.setGeometry(QtCore.QRect(10, 40, 150, 17))
        self.rb_phone.setMinimumSize(QtCore.QSize(150, 0))
        self.rb_phone.setObjectName("rb_phone")
        self.rb_date = QtWidgets.QRadioButton(self.groupBox)
        self.rb_date.setGeometry(QtCore.QRect(10, 60, 150, 17))
        self.rb_date.setMinimumSize(QtCore.QSize(150, 0))
        self.rb_date.setObjectName("rb_date")
        self.verticalLayout.addWidget(self.groupBox)
        self.btn_add = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_add.setObjectName("btn_add")
        self.verticalLayout.addWidget(self.btn_add)
        self.btn_show = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_show.setObjectName("btn_show")
        self.verticalLayout.addWidget(self.btn_show)
        self.btn_edit = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_edit.setObjectName("btn_edit")
        self.verticalLayout.addWidget(self.btn_edit)
        self.btn_del = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_del.setObjectName("btn_del")
        self.verticalLayout.addWidget(self.btn_del)
        self.save_list = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.save_list.setObjectName("save_list")
        self.verticalLayout.addWidget(self.save_list)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Записная книжка"))
        self.label.setText(_translate("MainWindow", "Список контактов:"))
        self.groupBox.setTitle(_translate("MainWindow", "сортировать"))
        self.rb_name.setText(_translate("MainWindow", "по фамилии"))
        self.rb_phone.setText(_translate("MainWindow", "по номеру телефона"))
        self.rb_date.setText(_translate("MainWindow", "по дате рождения"))
        self.btn_add.setText(_translate("MainWindow", "Добавить новый контакт"))
        self.btn_show.setText(_translate("MainWindow", "Показать данные контакта"))
        self.btn_edit.setText(_translate("MainWindow", "Редактировать данные контакта"))
        self.btn_del.setText(_translate("MainWindow", "Удалить выбранные контакты"))
        self.save_list.setText(_translate("MainWindow", "Скачать список контактов"))
