from PyQt5.QtWidgets import QTabWidget
from src.views.contact_chat_controller import ContactChatController
from PyQt5.QtWidgets import QTabWidget

from src.views.contact_chat_controller import ContactChatController


class TabChat(QTabWidget):
    """Класс главного окна чата,
     где находится список контактов"""

    def __init__(self, contact_chat, client):
        super().__init__()

        self.controller = ContactChatController(contact_chat, client)

    def my_addTab(self, contact_chat):
        self.addTab(contact_chat.frameSynthesis(), contact_chat.name)