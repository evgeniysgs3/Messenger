#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QApplication

from views.main_view import mainWindow


def main():
    app = QApplication(sys.argv)
    main_window = mainWindow()
    main_window.resize(400, 600)
    main_window.setWindowTitle("BirdHouse_v1.0")
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
