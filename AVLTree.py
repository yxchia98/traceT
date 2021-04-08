import pymongo as pymongo
from datetime import datetime

class AVLNode:
    left = None
    right = None
    height = 1
    id = None
    name = None
    phone = None
    covid = False
    covidtime = None

    def __init__(self, id, name, phone, covid, covidtime):
        self.id = id
        self.name = name
        self.phone = phone
        self.covid = covid
        self.covidtime = covidtime


class AVLTree:
    root = None
    preOrderArray = []
    inOrderArray = []
    postOrderArray = []
    casesArr = []

    def createAVL(self, a):
        self.root = None
        for x in a:
            self.root = self.avlPut(self.root, x['userID'], x['name'], x['phone'], x['covid'], x['covidtime'])

    def avlPut(self, node, id, name, phone, covid, covidtime):
        if node is None:
            return AVLNode(id, name, phone, covid, covidtime)
        if id < node.id:
            node.left = self.avlPut(node.left, id, name, phone, covid, covidtime)
        elif id > node.id:
            node.right = self.avlPut(node.right, id, name, phone, covid, covidtime)
        else:
            node.name = name
            node.phone = phone
            node.covid = covid
            node.covidtime = covidtime
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

    def newCase(self, id, db):
        node = self.root
        while node is not None:
            if id == node.id:
                node.covid = True
                node.covidtime = datetime.now()
                query = {'userID': id}
                newval = {'$set': {'covid': node.covid, 'covidtime': node.covidtime}}
                db.users.update_one(query, newval)
                return node
            elif id < node.id:
                node = node.left
            else:
                node = node.right
        return None

    def dismiss(self, id, db):
        node = self.root
        while node is not None:
            if id == node.id:
                node.covid = False
                node.covidtime = None
                query = {'userID': id, 'covidtime': node.covidtime}
                newval = {'$set': {'covid': node.covid, 'covidtime': None}}
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
        self.preOrderArray.append(node)
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
