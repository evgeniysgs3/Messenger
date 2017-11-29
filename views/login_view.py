from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QListWidget,QTabWidget, QWidget, QLabel, QVBoxLayout, QFrame, QTextEdit, QPushButton, QHBoxLayout, QDialog, QLineEdit, QMessageBox

class Login(QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.textName = QLineEdit(self)
        self.textPass = QLineEdit(self)
        self.buttonLogin = QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        layout = QVBoxLayout(self)
        layout.addWidget(self.textName)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)

    def handleLogin(self):
        if self.textName.text():
            self.accept()
        else:
            QMessageBox.warning(
                self, 'Error', 'Bad user or password')

    def get_login(self):
        return self.textName.text()