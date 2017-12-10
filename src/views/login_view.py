from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QListWidget,QTabWidget, QWidget, QLabel, QVBoxLayout, QFrame, QTextEdit, QPushButton, QHBoxLayout, QDialog, QLineEdit, QMessageBox
from socket import socket, AF_INET, SOCK_STREAM

class Login(QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)

        self.buttonLogin = QPushButton('Login', self)
        v_layout = QVBoxLayout(self)
        # Имя
        h_layout_name = QHBoxLayout(self)
        self.name = QLineEdit(self)
        self.l_name = QLabel("Name:")
        h_layout_name.addWidget(self.l_name)
        h_layout_name.addWidget(self.name)
        # Адрес
        h_layout_address = QHBoxLayout(self)
        self.server = QLineEdit('127.0.0.1')
        self.l_address = QLabel("Server:")
        h_layout_address.addWidget(self.l_address)
        h_layout_address.addWidget(self.server)
        # Порт
        h_layout_port = QHBoxLayout(self)
        self.port = QLineEdit('7777')
        self.l_port = QLabel("Port:")
        h_layout_port.addWidget(self.l_port)
        h_layout_port.addWidget(self.port)

        v_layout.addLayout(h_layout_name)
        v_layout.addLayout(h_layout_address)
        v_layout.addLayout(h_layout_port)
        v_layout.addWidget(self.buttonLogin)

        #connections
        self.buttonLogin.clicked.connect(self.handle_login)

    def handle_login(self):
        if self.name.text():
            try:
                #sock = socket(AF_INET, SOCK_STREAM)
                #sock.connect((self.server.text(), int(self.port.text())))
                #sock.close()
                self.accept()
            except OSError:
                QMessageBox.warning(
                    self, 'Error', 'Server is not available')
        else:
            QMessageBox.warning(
                self, 'Error', 'Bad user or password')

    def get_login(self):
        return self.name.text()

    def get_server(self):
        return self.server.text()

    def get_port(self):
        return int(self.port.text())