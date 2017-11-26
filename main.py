import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from views.client_view import Messanger
from views.client_controller import ControllerMessanger


class mainWindow(QMainWindow):
    """Вся основная работа начинется с этого класса
    Отвечает за отрисовку главного окна приложения и
    размещение в нем элементов

    """

    def __init__(self):
        """Конструктор создает экземпляры всех необходимых для
        работы классов
        И вызывается метод отрисовки и заполнения главного окна

        """

        super().__init__()

        self.vMessenger = Messanger()
        self.cMessanger = ControllerMessanger(self.vMessenger)
        self.init_UI()

    def init_UI(self):
        """Метод отрисовки главного окна приложения и
        заполнение его правильными элементами

        """

        self.hcentral = QHBoxLayout()
        self.hcentral.addWidget(self.vMessenger.frameSynthesis())

        self.central_widget = QWidget(self)
        self.central_widget.setLayout(self.hcentral)

        self.setCentralWidget(self.central_widget)
        self.show()
