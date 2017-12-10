from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget,QTabWidget, QWidget, QLabel, QVBoxLayout, QFrame, QTextEdit, QPushButton, QHBoxLayout
from PyQt5.QtCore import pyqtSlot

class ContactChatController(QWidget):

    def __init__(self, view_chat, client):
        super().__init__()

        self.view = view_chat
        self.client = client

        self.connections()

    def connections(self):
        self.view.btn_send_msg.clicked.connect(self.send_msg)

    @pyqtSlot()
    def send_msg(self):
        self.client.send_contact_msg(self.view.tb_message.toPlainText(), self.view.name)
        self.view.tb_message.clear()