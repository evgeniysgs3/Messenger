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

        self.connections()

    def connections(self):
        """Какой сигнал, какому слоту

        """

        self.view.list_contact_list.itemClicked.connect(self.createChatDialog)


    @pyqtSlot()
    def createChatDialog(self):
        """Создаем новое окно куда будут бобавляться все чаты"""
        self.chat = TabChat(ChatContact(), "new_tab")
        self.chat.show()
