class AdjNode:
    contact = None
    dateAndTime = None
    location = None
    bluetooth = None

    def __init__(self, contact, dateAndTime, location, bluetooth):
        self.contact = contact
        self.dateAndTime = dateAndTime
        self.location = location
        self.bluetooth = bluetooth
