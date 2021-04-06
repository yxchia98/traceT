class ContactNode:
    origin = None
    contacted = None
    dateAndTime = None
    location = None
    bluetooth = None

    def __init__(self, origin, contacted, dateAndTime, location, bluetooth):
        self.origin = origin
        self.contacted = contacted
        self.dateAndTime = dateAndTime
        self.location = location
        self.bluetooth = bluetooth

    def __eq__(self, other):
        if self.origin == other.origin or self.origin == other.contacted:
            if self.contacted == other.contacted or self.contacted == other.origin:
                if self.dateAndTime == other.dateAndTime:
                    if self.location == other.location:
                        return True
        return False
