from datetime import datetime
from datetime import timedelta
from random import randint
from random import randrange
from Graph import Graph
from ContactNode import getContacts
from AVLTree import AVLNode, AVLTree

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
            'covid': False
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
    location = ['Causeway Point', 'Hillion Mall', 'Changi Jewel', 'Northpoint City', 'Lot One', 'JCube', 'WestGate',
                'Vivo City', 'City Square Mall', 'Bugis+', 'Bedok Mall', 'Pulau Tekong']
    d1 = datetime.strptime('1/1/2008 00:00:00', '%m/%d/%Y %H:%M:%S')
    d2 = datetime.strptime('1/1/2009 23:59:59', '%m/%d/%Y %H:%M:%S')
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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    proceed = True
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
            '----------Main Menu----------\n1. Key in new confirmed case\n2. Get current cases\n3. De-register '
            'case\n4. Exit')
        choice = int(input('Enter choice: '))
        if choice == 1:
            print('Enter User ID of confirmed case, followed by close contacts')
            id = int(input('Enter User ID:'))
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
                print('\n1.Search for close contacts by ID\n2.Back to main menu')
                menu2choice = int(input('Enter Choice:'))
                if menu2choice == 1:
                    id = int(input('Enter ID:'))
                    contactGraph.printByID(id)
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
        elif choice == 9:
            arr = userAVL.inOrder(userAVL.root)
            for i in arr:
                print(i.id, i.name, i.phone, i.covid)
        else:
            proceed = False
