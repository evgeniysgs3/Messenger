import sys
from PyQt5 import QtGui, QtWidgets
from views.client import client


class Messenger(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = client.Ui_Messenger()
        self.ui.setupUi(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    messenger = Messenger()
    messenger.show()
    sys.exit(app.exec_())
