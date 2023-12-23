import sqlite3
import datetime

import self
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QInputDialog, QLineEdit, QWidget
import sys

class BasementUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Меню пропусков')
        self.setGeometry(555, 555, 555, 555)
        self.name_label = QLabel('Фамилия:')
        self.name_input = QLineEdit()
        self.surname_label = QLabel('Имя:')
        self.surname_input = QLineEdit()
        self.patronymic_label = QLabel('Отчество:')
        self.patronymic_input = QLineEdit()
        self.birthdate_label = QLabel('Дата рождения:')
        self.birthdate_input = QLineEdit()
        self.passnumber_label = QLabel('Номер пропуска:')
        self.passnumber_input = QLineEdit()
        self.check_button = QPushButton('Вход')
        self.check_button.clicked.connect(self.check_database)
        self.check_result = QLabel('')

        self.check_button1 = QPushButton('Выход')
        self.check_button1.clicked.connect(self.check_database_to_left)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.surname_label)
        self.layout.addWidget(self.surname_input)
        self.layout.addWidget(self.patronymic_label)
        self.layout.addWidget(self.patronymic_input)
        self.layout.addWidget(self.birthdate_label)
        self.layout.addWidget(self.birthdate_input)
        self.layout.addWidget(self.passnumber_label)
        self.layout.addWidget(self.passnumber_input)
        self.layout.addWidget(self.check_button)
        self.layout.addWidget(self.check_button1)
        self.layout.addWidget(self.check_result)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def check_database(self):
        surname = self.surname_input.text()
        name = self.name_input.text()
        patronymic = self.patronymic_input.text()
        birthdate = self.birthdate_input.text()
        passnumber = self.passnumber_input.text()
        if surname and name and patronymic and birthdate and passnumber:
            db_connection = sqlite3.connect('database.db')
            cursor = db_connection.cursor()
            cursor.execute(
                "SELECT * FROM database WHERE surname = ? AND name = ? AND patronymic = ? AND birthdate = ? AND number = ?",
                (surname, name, patronymic, birthdate,passnumber))
            database = cursor.fetchone()
            if database:
                self.check_result.setText('Работник вошёл.')
                time = datetime.datetime.now()
                cursor.execute(
                    "UPDATE database SET time_in = ? WHERE surname = ? AND name = ? AND patronymic = ? AND birthdate = ? AND number = ?",
                    (time, surname, name, patronymic, birthdate, passnumber))
                db_connection.commit()
            else:
                self.check_result.setText('Ошибка валидации')
            db_connection.close()
        else:
            self.check_result.setText('Внесите всю информацию о работнике')

    def check_database_to_left(self):
        surname = self.surname_input.text()
        name = self.name_input.text()
        patronymic = self.patronymic_input.text()
        birthdate = self.birthdate_input.text()
        passnumber = self.passnumber_input.text()
        if surname and name and patronymic and birthdate and passnumber:
            db_connection = sqlite3.connect('database.db')
            cursor = db_connection.cursor()
            cursor.execute(
                "SELECT * FROM database WHERE surname = ? AND name = ? AND patronymic = ? AND birthdate = ? AND number = ?",
                (surname, name, patronymic, birthdate,passnumber))
            database = cursor.fetchone()
            if database:
                self.check_result.setText('Сотрудник вышел с работы.')
                time_out = datetime.datetime.now()
                cursor.execute(
                    "UPDATE database SET time_out = ? WHERE surname = ? AND name = ? AND patronymic = ? AND birthdate = ? AND number = ?",
                    (time_out, surname, name, patronymic, birthdate,passnumber))
                db_connection.commit()
            else:
                self.check_result.setText('Сотрудник не прошёл проверку')
            db_connection.close()
        else:
            self.check_result.setText('Введите всю информацию')
if __name__ == '__main__':
    app = QApplication(sys.argv)
    basement_ui = BasementUI()
    basement_ui.show()
    sys.exit(app.exec())