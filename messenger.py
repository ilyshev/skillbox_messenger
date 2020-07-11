from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from clientui import Ui_MainWindow
import requests
import time


class ExampleApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, url):
        super().__init__()
        self.setupUi(self)
        # to run on button click:
        self.sendButton.pressed.connect(self.send_message)

        self.url = url

        self.after = time.time() - 24 * 60 * 60
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_messages)
        self.timer.start(1000)

    def format_message(self, message):
        name = message['name']
        text = message['text']
        dt = datetime.fromtimestamp(message['time'])
        dt_beauty = dt.strftime('%d/%m/%Y %H:%M:%S')
        return f'{name} {dt_beauty}\n{text}'

    def add_text(self, text):
        self.textBrowser.append(text)
        self.textBrowser.append('')
        self.textBrowser.repaint()

    def update_messages(self):
        try:
            response = requests.get(f'{self.url}messages',
                params={'after': self.after}
            )
        except:
            return
        messages = response.json()['messages']
        for message in messages:
            self.add_text(self.format_message(message))
            self.after = message['time']

    def send_message(self):
        name = self.lineEditName.text()
        password = self.lineEdiPassword.text()
        text = self.textEdit.toPlainText()
        if not name or not password or not text:
            self.add_text('Заполните данные')
            return
        message = {'name': name,
                   'password': password,
                   'text': text}
        try:
            response = requests.post(f'{self.url}send', json=message)
        except:
            self.add_text('Сервер недоступен')
            return
        if response.status_code == 200:
            self.textEdit.append('')
            self.textEdit.repaint()
        elif response.status_code == 400:
            self.add_text('Неверные name+password')
        else:
            self.add_text('Ошибка')


app = QtWidgets.QApplication([])
window = ExampleApp('http://127.0.0.1:5000/')
window.show()
app.exec_()
