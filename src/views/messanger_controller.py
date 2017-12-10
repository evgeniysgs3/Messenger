from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox
from .chat_view import TabChat
from .contact_chat_view import ChatContactView
from .contact_chat_controller import ContactChatController


class MessangerController(QWidget):
    """Контроллер чата

    """

    def __init__(self, view, client):
        """pass"""

        super().__init__()

        # self.client = client
        self.view = view

        self.client = client
        self.tab_chat = None

        self.list_chats = []

        self.connections()

    def connections(self):
        """Какой сигнал, какому слоту

        """

        self.view.list_contact_list.itemClicked.connect(self.create_chat_dialog)
        self.view.btn_refresh_contacts.clicked.connect(self.get_contacts)

    @pyqtSlot()
    def create_chat_dialog(self):
        """Создаем новое окно куда будут добавляться все чаты"""
        selected_contact = self.view.list_contact_list.currentItem().text()
        if self.tab_chat is None:
            self.first_chat = ChatContactView(selected_contact)
            self.tab_chat = TabChat(self.first_chat, self.client)
            self.tab_chat.my_addTab(self.first_chat)
            self.list_chats.append(self.first_chat.name)
        else:
            self.new_chat = ChatContactView(selected_contact)
            # ContactChatController(self.new_chat, self.client)
            if self.new_chat.name not in self.list_chats:
                self.list_chats.append(self.new_chat.name)
                self.tab_chat.my_addTab(self.new_chat)
        self.tab_chat.show()

    @pyqtSlot()
    def get_contacts(self):
        count_contacts, list_contact = self.client.get_contact_list_gui()
        if count_contacts == 0:
            QMessageBox.warning(
                self, 'Warning', 'You don`t have any contacts')
        else:
            self.view.list_contact_list.clear()
            for contact in list_contact:
                self.view.list_contact_list.addItem(contact)