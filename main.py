from random import randint

import pymongo as pymongo


class AVLNode:
    left = None
    right = None
    height = 1
    id = None
    name = None
    phone = None
    covid = False

    def __init__(self, id, name, phone, covid):
        self.id = id
        self.name = name
        self.phone = phone
        self.covid = covid


class AVLTree:
    root = None
    preOrderArray = []
    inOrderArray = []
    postOrderArray = []
    casesArr = []

    def createAVL(self, a):
        self.root = None
        for x in a:
            self.root = self.avlPut(self.root, x['userID'], x['name'], x['phone'], x['covid'])

    def avlPut(self, node, id, name, phone, covid):
        if node is None:
            return AVLNode(id, name, phone, covid)
        if id < node.id:
            node.left = self.avlPut(node.left, id, name, phone, covid)
        elif id > node.id:
            node.right = self.avlPut(node.right, id, name, phone, covid)
        else:
            node.name = name
            node.phone = phone
            node.covid = covid
        # update height of current node
        node.height = 1 + max(self.getHeight(node.left), self.getHeight(node.right))

        balance = self.getBalance(node)

        # left node contains more, inserted key is from left of left node
        if balance > 1 and id < node.left.id:
            return self.rotateRight(node)
        # right node contains more, inserted key is from right of right node
        if balance < -1 and id > node.right.id:
            return self.rotateLeft(node)
        # left node contains more, inserted key is from right of left node
        if balance > 1 and id > node.left.id:
            node.left = self.rotateLeft(node.left)
            return self.rotateRight(node)
        # right node contains more, inserted key is from left of right node
        if balance < -1 and id < node.right.id:
            node.right = self.rotateRight(node.right)
            return self.rotateLeft(node)
        return node

    # function to rotate left
    def rotateLeft(self, node):
        top = node.right
        bottom = top.left
        # perform rotation
        top.left = node
        node.right = bottom
        node.height = 1 + max(self.getHeight(node.left), self.getHeight(node.right))
        top.height = 1 + max(self.getHeight(top.left), self.getHeight(top.right))
        return top

    # function to rotate right
    def rotateRight(self, node):
        top = node.left
        bottom = top.right
        # perform rotation
        top.right = node
        node.left = bottom
        node.height = 1 + max(self.getHeight(node.left), self.getHeight(node.right))
        top.height = 1 + max(self.getHeight(top.left), self.getHeight(top.right))
        return top

    def getHeight(self, node):
        if not node:
            return 0
        return node.height

    def getBalance(self, node):
        if not node:
            return 0
        return self.getHeight(node.left) - self.getHeight(node.right)

    # given a id, return the id's node
    def getNode(self, id):
        node = self.root
        while node is not None:
            if id == node.id:
                return node
            elif id < node.id:
                node = node.left
            else:
                node = node.right
        return None

    def newCase(self, id):
        node = self.root
        while node is not None:
            if id == node.id:
                node.covid = True
                query = {'userID': id}
                newval = {'$set': {'covid': node.covid}}
                db.users.update_one(query, newval)
                return node
            elif id < node.id:
                node = node.left
            else:
                node = node.right
        return None

    def dismiss(self, id):
        node = self.root
        while node is not None:
            if id == node.id:
                node.covid = False
                query = {'userID': id}
                newval = {'$set': {'covid': node.covid}}
                db.users.update_one(query, newval)
                return node
            elif id < node.id:
                node = node.left
            else:
                node = node.right
        return None

    def getCases(self):
        # clear array first
        self.casesArr = []
        node = self.root
        self.getCases2(node)
        return self.casesArr

    def getCases2(self, node):
        if not node:
            return
        self.getCases2(node.left)
        if node.covid:
            self.casesArr.append(node)
        self.getCases2(node.right)

    # preOrder Traversal
    def preOrder(self, node):
        self.preOrderArray = []
        self.preOrder2(node)
        return self.preOrderArray

    def preOrder2(self, node):
        if not node:
            return
        arr.append(node)
        self.preOrder2(node.left)
        self.preOrder2(node.right)

    # inOrder Traversal
    def inOrder(self, node):
        self.inOrderArray = []
        self.inOrder2(node)
        return self.inOrderArray

    # populate array via in-order transversal
    def inOrder2(self, node):
        if not node:
            return
        self.inOrder2(node.left)
        self.inOrderArray.append(node)
        self.inOrder2(node.right)

    # postOrder Traversal
    def postOrder(self, node):
        self.postOrderArray = []
        self.postOrder2(node)
        return self.postOrderArray

    # populate array via post-order transversal
    def postOrder2(self, node):
        if not node:
            return
        self.postOrder2(node.left)
        self.postOrder2(node.right)
        self.postOrderArray.append(node)


class ContactNode:
    origin = None
    contacted = None
    date = None
    time = None
    location = None

    def __init__(self, origin, contacted, date, time, location):
        self.origin = origin
        self.contacted = contacted
        self.date = date
        self.time = time
        self.location = location

    def __eq__(self, other):
        if self.origin == other.origin or self.origin == other.contacted:
            if self.contacted == other.contacted or self.contacted == other.origin:
                if self.date == other.date:
                    if self.time == other.time:
                        if self.location == other.location:
                            return True
        return False


class AdjNode:
    contact = None
    date = None
    time = None
    location = None

    def __init__(self, contact, date, time, location):
        self.contact = contact
        self.date = date
        self.time = time
        self.location = location


class Graph:
    V = None
    graph = []

    def __init__(self, vertices):
        self.V = vertices
        self.graph = [None] * self.V

    def createGraph(self, a):
        self.graph = [None] * self.V
        for i in a:
            self.addEdge(i)

    def addEdge(self, source):
        # adding to origin node's list
        temp = AdjNode(source.contacted, source.date, source.time, source.location)
        # insert at head for linked list
        temp.next = self.graph[int(source.origin) - 1]
        self.graph[int(source.origin) - 1] = temp

        # adding to contacted node's list
        temp = AdjNode(source.origin, source.date, source.time, source.location)
        temp.next = self.graph[int(source.contacted) - 1]
        self.graph[int(source.contacted) - 1] = temp

    def printByID(self, id):
        temp = self.graph[id - 1]
        print('-----People in contact with UserID ' + str(id) + '-----')
        print("{: ^15} {: ^15} {: ^15} {: ^15}".format('UserID', 'Date', 'Time', 'Location'))
        while temp:
            print("{: ^15} {: ^15} {: ^15} {: ^15}".format(temp.contact, temp.date, temp.time, temp.location))
            temp = temp.next

    def printGraph(self):
        for i in range(self.V):
            print('UserID', i + 1, 'contacted: ', end=' ')
            temp = self.graph[i]
            while temp:
                print('->', temp.contact, end=' ')
                temp = temp.next
        print('\n')


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


def getContacts(a):
    arr = []
    for i in a:
        node = ContactNode(i['origin'], i['contacted'], i['date'], i['time'], i['location'])
        if node not in arr:
            arr.append(node)
    return arr


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
    # instantiate AVLTree for users
    userAVL = AVLTree()
    userAVL.createAVL(db.users.find())
    # get array of all contacts, in the form of ContactNodes
    contactArr = getContacts(db.contacts.find())
    # remove duplicates of personA-personB, to get undirected edges
    edgesArr = removeDupes(contactArr)
    # list of all users by in-order transversal.
    inOrderArr = userAVL.inOrder(userAVL.root)
    contactGraph = Graph(len(inOrderArr))
    for i in edgesArr:
        # print(i.origin, i.contacted, i.date, i.time, i.location)
        contactGraph.addEdge(i)
    # contactGraph.printGraph()
    print('Total number of users:', len(inOrderArr))
    while proceed:
        print(
            '----------Main Menu----------\n1. Key in new confirmed case\n2. Get current cases\n3. De-register case\n4. Exit')
        choice = int(input('Enter choice: '))
        if choice == 1:
            print('Enter User ID of confirmed case, followed by close contacts')
            id = int(input('Enter User ID:'))
            node = userAVL.newCase(id)
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
                    # print('User ID:', i.id, '\tName:', i.name, '\tMobile no.:', i.phone, '\tCovid status:', i.covid)
                print('\n1.Search for close contacts by ID\n2.Back to main menu')
                menu2choice = int(input('Enter Choice:'))
                if menu2choice == 1:
                    id = int(input('Enter ID:'))
                    contactGraph.printByID(id)
                    input('-----press any key to continue-----')
                else:
                    print('Clicked on 2')
                    menu2 = False
        elif choice == 3:
            print('Enter User ID of user to de-register')
            id = int(input('Enter User ID: '))
            node = userAVL.dismiss(id)
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
