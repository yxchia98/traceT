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

    # given a key, return the key's node
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

    # preOrder Traversal
    def preOrder(self, node):
        arr = []
        self.preOrder2(node, arr)
        return arr

    def preOrder2(self, node, arr):
        if not node:
            return
        arr.append(node)
        self.preOrder2(node.left, arr)
        self.preOrder2(node.right, arr)

    # inOrder Traversal
    def inOrder(self, node):
        arr = []
        self.inOrder2(node, arr)
        return arr

    # populate array via in-order transversal
    def inOrder2(self, node, arr):
        if not node:
            return
        self.inOrder2(node.left, arr)
        arr.append(node)
        self.inOrder2(node.right, arr)

    # postOrder Traversal
    def postOrder(self, node):
        arr = []
        self.postOrder2(node, arr)
        return arr

    # populate array via post-order transversal
    def postOrder2(self, node, arr):
        if not node:
            return
        self.postOrder2(node.left, arr)
        self.postOrder2(node.right, arr)
        arr.append(node)


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


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    client = pymongo.MongoClient(
        "mongodb+srv://Admin:UI0BvbxHM9F994HK@safetogether.wwfyn.mongodb.net/myFirstDatabase?retryWrites=true&w"
        "=majority")
    db = client.together
    # function to generate 500 users
    # print(generateUsers(500, db))
    userAVL = AVLTree()
    userAVL.createAVL(db.users.find())
    inOrderArr = userAVL.inOrder(userAVL.root)
    print(len(inOrderArr))
    for i in inOrderArr:
        print(i.id, i.name, i.phone, i.covid)
