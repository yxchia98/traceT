from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
import sys


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(200, 200, 300, 300)
    win.setWindowTitle("My first window!")

    label = QLabel(win)
    label.setText("my first label")
    label.move(50, 50)

    win.show()
    sys.exit(app.exec_())