from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget,QTabWidget, QWidget, QLabel, QVBoxLayout, QFrame, QTextEdit, QPushButton, QHBoxLayout

class ControllerContactChat(QWidget):

    def __init__(self, view_chat):
        super().__init__()

        self.view = view_chat

        self.connection()

    def connection(self):
        pass