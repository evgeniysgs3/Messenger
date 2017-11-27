from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QDialog
from views.chat_view import TabChat
from views.contact_chat import ChatContact


class ControllerMessanger(QWidget):
    """Контроллер чата

    """

    def __init__(self, view):
        """pass"""

        super().__init__()

        # self.client = client
        self.view = view

        self.tab_chat = None

        self.list_chats = []

        self.connections()

    def connections(self):
        """Какой сигнал, какому слоту

        """

        self.view.list_contact_list.itemClicked.connect(self.createChatDialog)


    @pyqtSlot()
    def createChatDialog(self):
        """Создаем новое окно куда будут бобавляться все чаты"""
        if self.tab_chat is None:
            self.first_chat = ChatContact("new_tab")
            self.tab_chat = TabChat(self.first_chat)
            self.tab_chat.my_addTab(self.first_chat)
            self.list_chats.append(self.first_chat.name)
        else:
            self.new_chat = ChatContact("new_tab2")
            if self.new_chat.name not in self.list_chats:
                self.list_chats.append(self.new_chat.name)
                self.tab_chat.my_addTab(self.new_chat)
        self.tab_chat.show()
