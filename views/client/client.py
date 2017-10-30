from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Messenger(object):

    def setupUi(self, Messenger):
        Messenger.setObjectName("Messenger")
        Messenger.resize(392, 455)
        self.centralwidget = QtWidgets.QWidget(Messenger)
        self.centralwidget.setObjectName("centralwidget")
        self.ListContact = QtWidgets.QListView(self.centralwidget)
        self.ListContact.setGeometry(QtCore.QRect(0, 0, 391, 361))
        self.ListContact.setObjectName("ListContact")

        self.TextMsg = QtWidgets.QTextEdit(self.centralwidget)
        self.TextMsg.setGeometry(QtCore.QRect(0, 360, 351, 51))
        self.TextMsg.setObjectName("TextMsg")
        self.retranslateUi(Messenger)
        QtCore.QMetaObject.connectSlotsByName(Messenger)

    def retranslateUi(self, Messenger):
        _translate = QtCore.QCoreApplication.translate
        Messenger.setWindowTitle(_translate("MainWindow", "Мессенджер"))