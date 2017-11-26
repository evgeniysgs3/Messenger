from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget,QTabWidget, QWidget, QLabel, QVBoxLayout, QFrame, QTextEdit, QPushButton, QHBoxLayout

class TabChat(QTabWidget):
    """Класс главного окна чата,
     где находится список контактов"""

    def __init__(self, contact_chat, contact_name):
        super().__init__()

        self.addTab(contact_chat.frameSynthesis(), contact_name)