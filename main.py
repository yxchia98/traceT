from datetime import datetime
from datetime import timedelta
from random import randint
from random import randrange
from Graph import Graph
from ContactNode import ContactNode
from AVLTree import AVLTree

import pymongo as pymongo



def generateUsers(num, db):
    db.users.drop()
    surname = ['Tan', 'Lim', 'Lee', 'Ng', 'Ong', 'Loong', 'Chia', 'Wong', 'Loh', 'Lor', 'Tang', 'Woo', 'Heng', 'Ang',
               'Chan']
    firstname = ['Andy', 'William', 'Benedict', 'John', 'Tom', 'Dick', 'Harry', 'Jerry', 'Peter', 'Jun Jie', 'Wei Jie',
                 'Brandon', 'Brenden', 'Kelly', 'Karen', 'Jessie', 'Julie', 'Annie', 'Melissa']
    for i in range(1, num + 1):
        user = {
            'userID': i,
            'name': firstname[randint(0, (len(firstname) - 1))] + ' ' + surname[randint(0, (len(surname) - 1))],
            'phone': 12345678,
            'covid': False,
            'covidtime': None
        }
        db.users.insert_one(user)
    return 'Inserted ' + str(num) + ' users'


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


def generateContacts(n, db):
    db.contacts.drop()
    location = ['Causeway Point', 'Hillion Mall', 'Changi Jewel', 'Northpoint City', 'LotOne', 'JCube', 'WestGate',
                'VivoCity', 'CitySquare Mall', 'Bugis+', 'Bedok Mall', 'Pulau Tekong']
    d1 = datetime.strptime('10/3/2021 00:00:00', '%d/%m/%Y %H:%M:%S')
    d2 = datetime.strptime('5/4/2021 23:59:59', '%d/%m/%Y %H:%M:%S')
    for i in range(n):
        print('i is currently', i)
        randomdatetime = random_date(d1, d2)
        personA = randint(1, 500)
        personB = randint(1, 500)
        while personB == personA:
            personB = randint(1, 500)
        contactlocation = location[randint(0, len(location) - 1)]
        bluetooth = -randint(30, 70)
        contact = {
            'origin': personA,
            'contacted': personB,
            'dateAndTime': randomdatetime,
            'location': contactlocation,
            'bluetooth': bluetooth
        }
        db.contacts.insert_one(contact)
        contact = {
            'origin': personB,
            'contacted': personA,
            'dateAndTime': randomdatetime,
            'location': contactlocation,
            'bluetooth': bluetooth
        }
        db.contacts.insert_one(contact)


def removeDupes(a):
    result = []
    for i in a:
        if i in result:
            continue
        result.append(i)
    return result


def getContacts(a):
    arr = []
    for i in a:
        node = ContactNode(i['origin'], i['contacted'], i['dateAndTime'], i['location'], i['bluetooth'])
        if node not in arr:
            arr.append(node)
    return arr


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    proceed = True  #enable this if you want to use console menu
    client = pymongo.MongoClient(
        "mongodb+srv://Admin:UI0BvbxHM9F994HK@safetogether.wwfyn.mongodb.net/myFirstDatabase?retryWrites=true&w"
        "=majority")
    db = client.together
    # function to generate 500 users
    # print(generateUsers(500, db))
    # generateContacts(2500, db)
    # instantiate AVLTree for users
    userAVL = AVLTree()
    userAVL.createAVL(db.users.find())
    # get array of all contacts, in the form of ContactNodes
    contactArr = getContacts(db.contacts.find())
    # remove duplicates of personA-personB, to get undirected edges
    # edgesArr = removeDupes(contactArr)
    # list of all users by in-order transversal.
    inOrderArr = userAVL.inOrder(userAVL.root)
    contactGraph = Graph(len(inOrderArr))
    for i in contactArr:
        contactGraph.addEdge(i)
    # contactGraph.printGraph()
    print('Total number of users:', len(inOrderArr))
    while proceed:
        print(
            '----------Main Menu----------\n1.Key in new confirmed case\n2.Get current cases\n3.De-register '
            'case\n4.Search by ID\n5.Exit')
        choice = int(input('Enter choice: '))
        if choice == 1:
            id = int(input('Enter User ID of confirmed case:'))
            node = userAVL.newCase(id, db)
            if node is None:
                print('Invalid User ID')
                continue
            print(node.id, node.name, node.phone, node.covid)
        elif choice == 2:
            menu2 = True
            while menu2:
                print('----------Current Cases----------')
                print("{: ^15} {: ^15} {: ^15} {: ^15}".format('UserID', 'Name', 'Mobile No.', 'Covid Status'))
                casesArr = userAVL.getCases()
                for i in casesArr:
                    print("{: ^15} {: ^15} {: ^15} {: ^15}".format(i.id, i.name, i.phone, str(i.covid)))
                print('\n1.Search for close contacts by ID\n2.Get all close contacts\n3.Back to main menu')
                menu2choice = int(input('Enter Choice:'))
                if menu2choice == 1:
                    id = int(input('Enter ID:'))
                    node = userAVL.getNode(id)
                    singleIDContacts = contactGraph.getContactByID(node)
                    print('-----People in contact with UserID ' + str(id) + '-----')
                    print("{: ^15} {: ^15} {: ^15} {: ^15} {: ^15}".format('UserID', 'Date', 'Time', 'Location',
                                                                           'Bluetooth strength'))
                    for i in singleIDContacts:
                        print("{: ^15} {: ^15} {: ^15} {: ^15} {: ^15} ".format(i.contact,
                                                                                i.dateAndTime.strftime('%d/%m/%Y'),
                                                                                i.dateAndTime.strftime('%H:%M'),
                                                                                i.location,
                                                                                str(i.bluetooth) + 'dBm'))
                    input('-----press any key to continue-----')
                elif menu2choice == 2:
                    closeContacts = contactGraph.getContactByArr(casesArr)
                    print('-----People with close contacts of postitive cases-----')
                    print("{: ^15} {: ^15} {: ^15} {: ^15} {: ^15}".format('UserID', 'Date', 'Time', 'Location',
                                                                           'Bluetooth strength'))
                    for i in closeContacts:
                        print("{: ^15} {: ^15} {: ^15} {: ^15} {: ^15} ".format(i.contact,
                                                                                i.dateAndTime.strftime('%d/%m/%Y'),
                                                                                i.dateAndTime.strftime('%H:%M'),
                                                                                i.location,
                                                                                str(i.bluetooth) + 'dBm'))
                    input('-----press any key to continue-----')
                else:
                    menu2 = False
        elif choice == 3:
            print('Enter User ID of user to de-register')
            id = int(input('Enter User ID: '))
            node = userAVL.dismiss(id, db)
            if node is None:
                print('Invalid User ID')
                continue
            print(node.id, node.name, node.phone, node.covid)

        elif choice == 4:
            id = int(input('Enter User ID to search for: '))
            node = userAVL.getNode(id)
            if node is None:
                print('Invalid User ID')
                continue
            print("{: ^15} {: ^15} {: ^15} {: ^15}".format('UserID', 'Name', 'Mobile No.', 'Covid Status'))
            print("{: ^15} {: ^15} {: ^15} {: ^15}".format(node.id, node.name, node.phone, str(node.covid)))

        elif choice == 9:
            arr = userAVL.inOrder(userAVL.root)
            for i in arr:
                print(i.id, i.name, i.phone, i.covid)
        else:
            proceed = False
