from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget, QWidget, QLabel, QVBoxLayout, QFrame, QTextEdit, QPushButton, QHBoxLayout, QLayout, QScrollArea

class MessangerView(QWidget):
    """Класс главного окна чата,
     где находится список контактов"""

    def __init__(self):
        super().__init__()

        self.list_contact_list = QListWidget()
        self.btn_refresh_contacts = QPushButton("Обновить")
        self.qtxt_edit_inbox_msg = QTextEdit()



    def __frame_contact_list(self):

        # Здесь будет находиться список контактов
        self.l_contact_list = QLabel("Список контактов:")

        self.list_contact_list
        #self.list_contact_list.addItem("test")
        #self.list_contact_list.addItem("tet2")

        self.vbox_contact_list = QVBoxLayout()
        self.vbox_contact_list.addWidget(self.l_contact_list)
        self.vbox_contact_list.addWidget(self.btn_refresh_contacts)
        self.vbox_contact_list.addWidget(self.list_contact_list)

        self.frame_contact_list = QFrame()
        self.frame_contact_list.setFrameShape(QFrame.Panel)
        self.frame_contact_list.setFrameShadow(QFrame.Sunken)
        self.frame_contact_list.setLayout(self.vbox_contact_list)

        return self.frame_contact_list

    def __frame_write_and_send_msg(self):
        """Фрейм написания и отправки сообщения"""

        # self.l_send_group_msg = QLabel("Групповое сообщение:")
        # self.tb_message = QTextEdit()
        # self.btn_send_msg = QPushButton("Отпарвить")
        #
        # self.hbox_send_msg = QHBoxLayout()
        # self.hbox_send_msg.addWidget(self.tb_message)
        # self.hbox_send_msg.addWidget(self.btn_send_msg)
        #
        # self.vbox_send_msg = QVBoxLayout()
        # self.vbox_send_msg.addWidget(self.l_send_group_msg)
        # self.vbox_send_msg.addLayout(self.hbox_send_msg)
        #
        # self.frame_send_msg = QFrame()
        # self.frame_send_msg.setFrameShape(QFrame.Panel)
        # self.frame_send_msg.setFrameShadow(QFrame.Sunken)
        # self.frame_send_msg.setLayout(self.vbox_send_msg)
        #
        # return self.frame_send_msg
        pass

    def __frame_inbox_msg(self):
        """Фрейм написания и отправки сообщения"""

        self.l_inbox_msg = QLabel("Входящие сообщения:")
        self.qtxt_edit_inbox_msg.setReadOnly(True)

        self.vbox_inbox_msg = QVBoxLayout()
        self.vbox_inbox_msg.addWidget(self.l_inbox_msg)
        self.vbox_inbox_msg.addWidget(self.qtxt_edit_inbox_msg)

        self.frame_inbox_msg = QFrame()
        self.frame_inbox_msg.setFrameShape(QFrame.Panel)
        self.frame_inbox_msg.setFrameShadow(QFrame.Sunken)
        self.frame_inbox_msg.setLayout(self.vbox_inbox_msg)

        return self.frame_inbox_msg

    def frameSynthesis(self):
        """Метод, возвращающий виджет основного окна мессенджера,
        на которой осуществляется вывод входящих сообщений

        """

        self.vbox_synthesis = QVBoxLayout()
        self.vbox_synthesis.addWidget(self.__frame_contact_list(), 3)
        self.vbox_synthesis.addWidget(self.__frame_inbox_msg(), 6)

        self.frame_synthesis = QFrame()
        self.frame_synthesis.setLayout(self.vbox_synthesis)

        return self.frame_synthesis