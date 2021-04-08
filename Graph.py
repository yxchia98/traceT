from AdjacentNode import AdjNode
from datetime import datetime, timedelta


class Graph:
    V = None
    graph: list = []

    def __init__(self, vertices):
        self.V = vertices
        self.graph = [None] * self.V

    def createGraph(self, a):
        self.graph = [None] * self.V
        for i in a:
            self.addEdge(i)

    def addEdge(self, source):
        # adding to origin node's list
        temp = AdjNode(source.contacted, source.dateAndTime, source.location, source.bluetooth)
        # insert at head for linked list
        temp.next = self.graph[int(source.origin) - 1]
        self.graph[int(source.origin) - 1] = temp

        # adding to contacted node's list
        temp = AdjNode(source.origin, source.dateAndTime, source.location, source.bluetooth)
        temp.next = self.graph[int(source.contacted) - 1]
        self.graph[int(source.contacted) - 1] = temp

    def getContactByID(self, node):
        arr = []
        if node.id > len(self.graph):
            print('Invalid ID Entered')
            return arr
        temp = self.graph[node.id - 1]
        while temp:
            if (node.covidtime - timedelta(days=14)) < temp.dateAndTime < node.covidtime:
                arr.append(temp)
            temp = temp.next
        return arr

    def getContactByArr(self, n: list):
        arr = []
        for i in n:
            temp = self.graph[int(i.id) - 1]
            while temp:
                if (i.covidtime - timedelta(days=14)) < temp.dateAndTime < i.covidtime:
                    arr.append(temp)
                temp = temp.next
        return arr

    def printGraph(self):
        for i in range(self.V):
            print('UserID', i + 1, 'contacted: ', end=' ')
            temp = self.graph[i]
            while temp:
                print('->', temp.contact, end=' ')
                temp = temp.next
            print('\n')
