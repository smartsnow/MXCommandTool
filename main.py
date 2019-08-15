#!/usr/bin/env python3
# author snowyang

import sys
import qdarkstyle
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont, QIcon
from mainWindow import MainWindow
from worker import Worker

if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setFont(QFont("Calibri"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    app.setWindowIcon(QIcon('logo.png'))
    # app.setStyleSheet(open('style.css').read())
    win = MainWindow()
    win.show()
    worker = Worker(win)
    worker.start()
    sys.exit(app.exec_())
