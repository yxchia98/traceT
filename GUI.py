import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from AVLTree import AVLTree
import pymongo as pymongo
from Graph import Graph
from ContactNode import ContactNode
from messenger import *


def getContacts(a):
    arr = []
    for i in a:
        node = ContactNode(i['origin'], i['contacted'], i['dateAndTime'], i['location'], i['bluetooth'])
        if node not in arr:
            arr.append(node)
    return arr


def dialog():
    input = textbox.text()
    node = userAVL.newCase(int(input), db)
    mbox = QMessageBox()
    mbox.setWindowTitle("Update")
    mbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    if node is None:
        mbox.setText("Invalid id")
    else:
        mbox.setText("The information has been updated")
        casesArr = userAVL.getCases()
        infectedCount = len(casesArr)
        result.setText(str(infectedCount))
        text = "{: ^15} {: ^15} {: ^15} {: ^15} {: ^15}".format('UserID', 'Name', 'Mobile No.', 'Covid Status',
                                                                'Infection Date')
        for i in casesArr:
            timestring = i.covidtime.strftime('%d/%m/%Y')
            text += "\n{: ^15} {: ^15} {: ^15} {: ^15} {: ^15}".format(i.id, i.name, i.phone, str(i.covid),
                                                                       timestring)
        currentcasestext.setPlainText(text)
        mbox.exec_()

def dialog1():
    input = textbox1.text()
    node = userAVL.dismiss(int(input), db)
    mbox = QMessageBox()
    mbox.setWindowTitle("Update")
    mbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    if node is None:
        mbox.setText("Invalid id")
    else:
        mbox.setText("The information has been updated")
        casesArr = userAVL.getCases()
        infectedCount = len(casesArr)
        result.setText(str(infectedCount))
        text = "{: ^15} {: ^15} {: ^15} {: ^15} {: ^15}".format('UserID', 'Name', 'Mobile No.', 'Covid Status',
                                                                'Infection Date')
        for i in casesArr:
            timestring = i.covidtime.strftime('%d/%m/%Y')
            text += "\n{: ^15} {: ^15} {: ^15} {: ^15} {: ^15}".format(i.id, i.name, i.phone, str(i.covid),
                                                                       timestring)
        currentcasestext.setPlainText(text)
    mbox.exec_()

def search():
    input = textbox2.text()
    node = userAVL.getNode(int(input))
    mbox = QMessageBox()
    mbox.setWindowTitle("Update")
    mbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    if node is None:
        mbox.setText("Invalid ID")
    elif node.covidtime:
        mbox.setText("Details for userID " + str(node.id))
        mbox.setDetailedText("UserID: " + str(node.id) + "\nName: " + str(node.name) + "\nMobile no.: " + str(node.phone) + "\nCovid Status: " + str(node.covid) + "\nInfection Time: "
                             + node.covidtime.strftime('%d/%m/%Y') + ', ' + node.covidtime.strftime('%H:%M'))
    else:
        mbox.setText("Details for userID " + str(node.id))
        mbox.setDetailedText("UserID: " + str(node.id) + "\nName: " + str(node.name) + "\nMobile no.: " + str(
            node.phone) + "\nCovid Status: " + str(node.covid) + "\nInfection Time: "
                             + str(node.covidtime))
    mbox.exec_()

def sendalert():
    sendable = False
    input = int(textbox3.text())
    smsbox = QMessageBox()
    smsbox.setWindowTitle("Send Alert")
    smsbox.setStandardButtons(QMessageBox.Ok)
    for i in closeContactsarr:
        if input == i.contact:
            sendable = True

    if sendable:
        node = userAVL.getNode(input)
        mobile = '+65' + str(node.phone)
        msg = Messenger('AC529796f7c206f315a9c2afdaba05adb1', '')
        msg.send(
            'Dear Sir/Madam. You have been in close contact with someone who has COVID-19. Self isolate for 14 days and get yourself tested in the following locations near you at www.onemap.gov.sg/main/v2/pcrtmap/',
            '+14439988401', mobile)
        smsbox.setText('SMS alert sent!')
    else:
        smsbox.setText('User is not a close contact')

    smsbox.exec_()



def closeContacts():
    box = QMessageBox()
    casesArr = userAVL.getCases()
    closeContactsarr = contactGraph.getContactByArr(casesArr)
    box.setWindowTitle("Close Contacts")
    boxtext = "{: ^15} {: ^15} {: ^15} {: ^15} {: ^15}".format('UserID', 'Date', 'Time', 'Location',
                                                                           'Bluetooth strength')
    for i in closeContactsarr:
        boxtext += "\n{: ^15} {: ^15} {: ^15} {: ^15} {: ^15} ".format(i.contact,
                                                                                i.dateAndTime.strftime('%d/%m/%Y'),
                                                                                i.dateAndTime.strftime('%H:%M'),
                                                                                i.location,
                                                                                str(i.bluetooth) + 'dBm')
    box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    box.setText("\tClose contacts with Covid-postive users \t\t")
    box.setDetailedText(boxtext)

    box.exec_()

if __name__ == "__main__":
    proceed = True
    client = pymongo.MongoClient(
        "mongodb+srv://Admin:UI0BvbxHM9F994HK@safetogether.wwfyn.mongodb.net/myFirstDatabase?retryWrites=true&w"
        "=majority")
    db = client.together
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    w = QWidget()
    w.resize(800, 600)
    w.setWindowTitle('Trace Together')
    layout = QVBoxLayout()
    userAVL = AVLTree()
    userAVL.createAVL(db.users.find())
    casesArr = userAVL.getCases()
    infectedCount = len(casesArr)
    text = "{: ^15} {: ^15} {: ^15} {: ^15} {: ^15}".format('UserID', 'Name', 'Mobile No.', 'Covid Status', 'Infection Date')
    for i in casesArr:
        timestring = i.covidtime.strftime('%d/%m/%Y')
        text += "\n{: ^15} {: ^15} {: ^15} {: ^15} {: ^15}".format(i.id, i.name, i.phone, str(i.covid),
                                                                   timestring)
    contactArr = getContacts(db.contacts.find())
    inOrderArr = userAVL.inOrder(userAVL.root)
    contactGraph = Graph(len(inOrderArr))
    for i in contactArr:
        contactGraph.addEdge(i)

    closeContactsarr = contactGraph.getContactByArr(casesArr)


    title = QtWidgets.QLabel(w)
    title.setText("Trace Together Project")
    title.setFont(QFont('Arial', 30))
    title.move(190, 20)
    title.setAlignment(Qt.AlignCenter)
    title.setStyleSheet("QLabel {color: white; background-color: Orange; padding: 15px;}")
    # title.adjustSize()


    title1 = QtWidgets.QLabel(w)
    title1.setText("Number of Covid Cases: ", )
    title1.setFont(QFont('Arial', 14))
    title1.move(50, 200)
    title1.setStyleSheet("QLabel {color: white; background-color: Orange; padding: 15px;}")
    title1.adjustSize()

    result = QtWidgets.QLabel(w)
    result.setText(str(infectedCount))
    result.move(298, 200)
    result.setStyleSheet("QLabel {color: black; background-color: Orange; padding: 19px;}")
    result.adjustSize()


    currentcasestitle = QtWidgets.QLabel(w)
    currentcasestitle.setText("Current cases")
    currentcasestitle.setFont(QFont('Arial', 14))
    currentcasestitle.move(520, 150)
    title.setAlignment(Qt.AlignRight)
    currentcasestitle.setStyleSheet("QLabel {color: white; background-color: Orange; padding: 15px;}")

    currentcasestext = QTextEdit(w)
    currentcasestext.setReadOnly(True)
    currentcasestext.resize(350, 350)
    currentcasestext.setFont(QFont('Arial', 8))
    currentcasestext.move(420, 210)
    currentcasestext.setPlainText(text)

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
    btn1.clicked.connect(dialog1)

    #Search function
    textbox2 = QLineEdit(w)
    textbox2.move(50, 420)
    textbox2.resize(200, 30)
    textbox2.show()

    btn2 = QPushButton(w)
    btn2.setText('Search person by ID')
    btn2.move(270, 422)
    btn2.show()
    btn2.clicked.connect(search)

    textbox3 = QLineEdit(w)
    textbox3.move(50, 480)
    textbox3.resize(200, 30)
    textbox3.show()

    btn3 = QPushButton(w)
    btn3.setText('Send alert by ID')
    btn3.move(270, 482)
    btn3.show()
    btn3.clicked.connect(sendalert)

    btn4 = QPushButton(w)
    btn4.setText('Show Close Contacts')
    btn4.move(150, 530)
    btn4.resize(150, 50)
    btn4.setStyleSheet("QPushButton {color: white; background-color: Orange; padding: 5px;}")
    btn4.clicked.connect(closeContacts)
    w.show()
    sys.exit(app.exec_())
