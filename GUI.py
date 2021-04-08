import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from AVLTree import AVLTree
import pymongo as pymongo


def dialog():
    print(textbox2.text())
    input = int(textbox2.text())
    node = userAVL.newCase(input, db)
    mbox = QMessageBox()
    mbox.setWindowTitle("Update")
    mbox.setText("The information has been updated")
    mbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    mbox.exec_()


if __name__ == "__main__":
    proceed = True
    client = pymongo.MongoClient(
        "mongodb+srv://Admin:UI0BvbxHM9F994HK@safetogether.wwfyn.mongodb.net/myFirstDatabase?retryWrites=true&w"
        "=majority")
    db = client.together
    app = QApplication(sys.argv)
    w = QWidget()
    w.resize(800, 600)
    w.setWindowTitle('Trace Together')


    title = QtWidgets.QLabel(w)
    title.setText("Trace Together Project")
    title.setFont(QFont('Arial', 30))
    title.move(190, 20)
    title.setAlignment(Qt.AlignCenter)
    title.setStyleSheet("QLabel {color: white; background-color: Orange; padding: 15px;}")
    title.adjustSize()


    title1 = QtWidgets.QLabel(w)
    title1.setText("Number of Covid Cases: ", )
    title1.setFont(QFont('Arial', 14))
    title1.move(50, 200)
    title1.setStyleSheet("QLabel {color: white; background-color: Orange; padding: 15px;}")
    title1.adjustSize()


    result = QtWidgets.QLabel(w)
    userAVL = AVLTree()
    userAVL.createAVL(db.users.find())
    casesArr = len(userAVL.getCases())
    result.setText(str(casesArr))
    result.move(298, 200)
    result.setStyleSheet("QLabel {color: black; background-color: Orange; padding: 19px;}")
    result.adjustSize()

    #New case
    textbox = QLineEdit(w)
    textbox.move(50, 300)
    textbox.resize(200, 30)
    textbox.show()

    btn = QPushButton(w)
    btn.setText('Update a confirmed case')
    btn.move(270, 303)
    btn.show()
    btn.clicked.connect(dialog)

    #Recovered case
    textbox1 = QLineEdit(w)
    textbox1.move(50, 360)
    textbox1.resize(200, 30)
    textbox1.show()

    btn1 = QPushButton(w)
    btn1.setText('Update a recovered case')
    btn1.move(270, 363)
    btn1.show()
    btn1.clicked.connect(dialog)

    #Search function
    textbox2 = QLineEdit(w)
    textbox2.move(50, 420)
    textbox2.resize(200, 30)
    textbox2.show()

    btn2 = QPushButton(w)
    btn2.setText('Search person by ID')
    btn2.move(270, 422)
    btn2.show()
    btn2.clicked.connect(dialog)

    w.show()
    sys.exit(app.exec_())