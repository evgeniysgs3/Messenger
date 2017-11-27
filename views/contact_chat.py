from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget, QScrollArea, QWidget, QLabel, QVBoxLayout, QFrame, QTextEdit, QPushButton, QHBoxLayout

class ChatContact(QWidget):
    """Класс главного окна чата,
     где находится список контактов"""

    def __init__(self, contact_name):
        super().__init__()
        self.name = contact_name
        self.frameSynthesis()

    def __repr__(self):
        return "%s" % (self.contact_name)

    def __frame_history(self):
        self.l_history = QLabel("История переписки:")
        self.scroll_history = QScrollArea()

        self.vbox_history = QVBoxLayout()
        self.vbox_history.addWidget(self.l_history)
        self.vbox_history.addWidget(self.scroll_history)

        self.frame_history = QFrame()
        self.frame_history.setFrameShape(QFrame.Panel)
        self.frame_history.setFrameShadow(QFrame.Sunken)
        self.frame_history.setLayout(self.vbox_history)

        return self.frame_history

    def __frame_write_and_send_msg(self):
        """Фрейм написания и отправки сообщения"""

        self.tb_message = QTextEdit()
        self.btn_send_msg = QPushButton("Отпарвить")

        self.hbox_send_msg = QHBoxLayout()
        self.hbox_send_msg.addWidget(self.tb_message)
        self.hbox_send_msg.addWidget(self.btn_send_msg)
        self.frame_send_msg = QFrame()
        self.frame_send_msg.setFrameShape(QFrame.Panel)
        self.frame_send_msg.setFrameShadow(QFrame.Sunken)
        self.frame_send_msg.setLayout(self.hbox_send_msg)

        return self.frame_send_msg

    def frameSynthesis(self):
        """Метод, возвращающий виджет основного окна мессенджера,
        на которой осуществляется работа с картой

        """

        self.vbox_synthesis = QVBoxLayout()
        self.vbox_synthesis.addWidget(self.__frame_history(), 6)
        self.vbox_synthesis.addWidget(self.__frame_write_and_send_msg(), 3)

        self.frame_synthesis = QFrame()
        self.frame_synthesis.setLayout(self.vbox_synthesis)

        return self.frame_synthesis