from rasa.shared.core.slots import Slot

class Event(Slot):
    def __init__(self, time_key, name, location):
        self.time_key=time_key
        self.name=name
        self.location=location



