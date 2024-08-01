class Event:
    def __init__(self, minute, name, location):
        self.minute=minute
        self.name=name
        self.location=location
class Day:
    events = []


class Calendar:

    list_of_days = []
    for i in range(365):
        list_of_days.append(Day())

    @classmethod
    def addEvent(cls, day_num, event_name, event_time, event_location):
        new_event = Event(event_time, event_name, event_location)
        cls.list_of_days[day_num].events.append(new_event)
    
    @classmethod
    def printEvent(cls, day_num, event_time=-1):
        return cls.list_of_days[day_num].events[0].name

cal = Calendar()
cal.addEvent(275, "Fishing", 383, "Fishing Pond")
print(cal.printEvent(275, 383))    