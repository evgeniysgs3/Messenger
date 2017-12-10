from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QAction

from src.client.main import Client
from .messanger_controller import MessangerController
from .messanger_view import MessangerView
from src.views.add_contact_view import NewContact
from src.views.add_contact_controller import AddContactController


class mainWindow(QMainWindow):
    """Вся основная работа начинется с этого класса
    Отвечает за отрисовку главного окна приложения и
    размещение в нем элементов

    """

    def __init__(self, login, server, port):
        """Конструктор создает экземпляры всех необходимых для
        работы классов
        И вызывается метод отрисовки и заполнения главного окна

        """

        super().__init__()

        self.client = Client(login)
        self.client.start_gui_client(server, port)

        self.client.listener.gotMsg.connect(self.show_inbox_msg)

        self.v_messenger = MessangerView()
        self.c_messanger = MessangerController(self.v_messenger, self.client)

        self.v_add_contact = NewContact()
        self.c_add_new_contact = AddContactController(self.v_add_contact, self.client)

        self.init_UI()

    def init_UI(self):
        """Метод отрисовки главного окна приложения и
        заполнение его правильными элементами

        """

        #Меню
        add_contact_action = QAction('Добавить контакт', self)
        add_contact_action.setShortcut('Ctrl+A')
        add_contact_action.setStatusTip('Add contact')
        add_contact_action.triggered.connect(self.add_contact)

        self.statusBar()

        toolbar = self.addToolBar('Add Contact')
        toolbar.addAction(add_contact_action)

        #Список контактов

        self.hcentral = QHBoxLayout()
        self.hcentral.addWidget(self.v_messenger.frameSynthesis())

        self.central_widget = QWidget(self)
        self.central_widget.setLayout(self.hcentral)

        self.setCentralWidget(self.central_widget)
        #self.show()

    @pyqtSlot()
    def add_contact(self):
        self.v_add_contact.show()
        #new_contact.add_contact()

    @pyqtSlot(str)
    def show_inbox_msg(self, data):
        ''' Отображение сообщения в истории
            '''
        try:
            msg = data
            self.v_messenger.qtxt_edit_inbox_msg.append(msg)
        except Exception as e:
            print(e)