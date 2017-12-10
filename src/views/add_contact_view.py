from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QListWidget,QTabWidget, QWidget, QLabel, QVBoxLayout, QFrame, QTextEdit, QPushButton, QHBoxLayout, QDialog, QLineEdit, QMessageBox
from socket import socket, AF_INET, SOCK_STREAM

class NewContact(QDialog):
    def __init__(self):
        super().__init__()

        self.btn_add_contact = QPushButton('Add', self)
        v_layout = QVBoxLayout(self)
        # Имя
        h_layout_name = QHBoxLayout(self)
        self.new_contact_name = QLineEdit(self)
        self.l_new_contact_name = QLabel("Name:")
        h_layout_name.addWidget(self.l_new_contact_name)
        h_layout_name.addWidget(self.new_contact_name)

        v_layout.addLayout(h_layout_name)
        v_layout.addWidget(self.btn_add_contact)

