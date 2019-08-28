#!/usr/bin/env python3
# author snowyang

import sys
import qdarkstyle
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from mainWindow import MainWindow

if __name__ == "__main__":

    app = QApplication(sys.argv)
    splash = QSplashScreen(QPixmap("resources/start.png"))
    splash.showMessage("Loading ...", Qt.AlignHCenter | Qt.AlignBottom, Qt.white)
    splash.show()
    splash.repaint()
    app.setFont(QFont("Calibri"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5().replace('min-height: 1.25em;', ''))
    app.setWindowIcon(QIcon("resources/logo.png"))
    win = MainWindow()
    win.show()
    splash.finish(win)
    sys.exit(app.exec_())
