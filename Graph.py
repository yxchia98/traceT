from AdjacentNode import AdjNode

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

    def getContactByID(self, id):
        n = []
        temp = self.graph[id - 1]
        # print('-----People in contact with UserID ' + str(id) + '-----')
        # print("{: ^15} {: ^15} {: ^15} {: ^15} {: ^15}".format('UserID', 'Date', 'Time', 'Location', 'Bluetooth strength'))
        while temp:
            n.append(temp)
            # print(temp.contact, temp.dateAndTime.strftime('%d/%m/%Y %H:%M:%S'), temp.location, temp.bluetooth)
            # print("{: ^15} {: ^15} {: ^15} {: ^15} {: ^15} ".format(temp.contact, temp.dateAndTime.strftime('%d/%m/%Y'), temp.dateAndTime.strftime('%H:%M'), temp.location, str(temp.bluetooth) + 'dBm'))
            temp = temp.next
        return n

    def printGraph(self):
        for i in range(self.V):
            print('UserID', i + 1, 'contacted: ', end=' ')
            temp = self.graph[i]
            while temp:
                print('->', temp.contact, end=' ')
                temp = temp.next
        print('\n')
