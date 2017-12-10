from PyQt5.QtWidgets import QListWidget,QTabWidget, QWidget, QLabel, QVBoxLayout, QFrame, QTextEdit, QPushButton, QHBoxLayout
from PyQt5.QtCore import pyqtSlot

class AddContactController(QWidget):

    def __init__(self, view_new_contact, client):
        super().__init__()

        self.view = view_new_contact
        self.client = client

        self.connections()

    def connections(self):
        self.view.btn_add_contact.clicked.connect(self.add_contact)

    @pyqtSlot()
    def add_contact(self):
        self.view.show()
        self.client.add_contact(self.view.new_contact_name.text())