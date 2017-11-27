from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget,QTabWidget, QWidget, QLabel, QVBoxLayout, QFrame, QTextEdit, QPushButton, QHBoxLayout

class TabChat(QTabWidget):
    """Класс главного окна чата,
     где находится список контактов"""

    def __init__(self, contact_chat):
        super().__init__()

    def my_addTab(self, contact_chat):
        self.addTab(contact_chat.frameSynthesis(), contact_chat.name)