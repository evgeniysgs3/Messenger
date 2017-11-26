#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication
from main import mainWindow


def main():
    app = QApplication(sys.argv)
    main_window = mainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
