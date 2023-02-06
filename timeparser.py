class Time:
    def __init__(self, string):
        self.calendar = {"Jan":1, "Feb":2,
                    "Mar":3, "Apr":4,
                    "May":5, "Jun":6,
                    "Jul":7, "Aug":8,
                    "Sep":9, "Oct":10,
                    "Nov":11, "Dec":12}
        data = string.split()
        self.year = int(data[3])
        self.month = self.calendar[data[2]]
        self.day = int(data[1])
        data2 = data[4].split(":")
        self.hours = int(data2[0])
        self.minutes = int(data2[1])
        self.seconds = int(data2[2])


    def in_seconds(self):
        return (self.year*31556926
        + self.month*2629744
        + self.day*86400
        + self.hours*3600
        + self.minutes*60
        + self.seconds)
        
    def __gt__(self, other):
        return  self.in_seconds() > other.in_seconds()

    def __lt__(self, other):
        return  self.in_seconds() < other.in_seconds()

    def __eq__(self, other):
        return  self.in_seconds() == other.in_seconds()

    def __ge__(self, other):
        return  self.in_seconds() >= other.in_seconds()

    def __le__(self, other):
        return  self.in_seconds() <= other.in_seconds()
    
