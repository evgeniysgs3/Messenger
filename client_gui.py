import sys

from PyQt5.QtWidgets import QApplication, QDialog
from src.views.login_view import Login
from src.views.main_view import mainWindow

def main():
    app = QApplication(sys.argv)
    login = Login()
    if login.exec_() == QDialog.Accepted:
        main_window = mainWindow(login.get_login(), login.get_server(), login.get_port())
        main_window.resize(400, 600)
        main_window.setWindowTitle("BirdHouse_v1.0")
        main_window.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    main()
