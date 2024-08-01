# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from datetime import datetime

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from pymongo import MongoClient
from rasa_sdk.events import SlotSet




# class ActionHelloWorld(Action):

#     def name(self) -> Text:
#         return "action_hello_world"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hello World!")

#         return []


class TestEvent(Action):

    def name(self) -> Text:
        return "TestEvent"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Test Custom Action Success")

        return []

class ActionReturnEvent(Action):
    def name(self) -> Text:
        return "ActionReturnEvent"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        time_tier = 0
        client = MongoClient('mongodb+srv://kevinyin:Anbo%400104@cluster0.4fz5pbg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

        #db=client.test_databases
        now = datetime.now()
        
        now = str(now)

        year = now[:4]
        month = now[5:-19]
        day = now[8:-16]
        time = now[11:-10]

        collection = client['Personal']['events']

        event_year = tracker.get_slot("event_year")
        if event_year != 0.0:
            time_tier = 1 #year=1
        else:
            event_year = year
        event_month = tracker.get_slot("event_month")
        if event_month != 0.0:
            time_tier = 2 #month=2
        else:
            event_month = month
        event_day = tracker.get_slot("event_day")
        if event_day != 0.0:
            time_tier = 3 #day=3
        else:
            event_day = day
        event_time = tracker.get_slot("event_time")
        if event_time != "":
            time_tier = 4 #time=4
        else:
            event_time = time
        event_name = tracker.get_slot("event_name_ent")
        if event_name != "":
            #dispatcher.utter_message("Event name is ", event_name)
            time_tier = 5 #name=5
        event_location = tracker.get_slot("event_location")
        if event_location != "":
            #dispatcher.utter_template("Event location is ", event_location)
            time_tier = 6 #location=6
        dispatcher.utter_message(text=f"time tier is {time_tier}")

        #dispatcher.utter_message(text=f"the slot for event month is set to {event_month}")
        if time_tier == 1: #for year, return name and month
            name_month_result = collection.find({"year": int(event_year)}, {"name":1, "month":1, "_id":0})
            if name_month_result:
                for event_name_list in name_month_result:
                    dispatcher.utter_message(text=f"In {list(event_name_list.values())[1]}, you have {list(event_name_list.values())[0]}\n")
            else:
                dispatcher.utter_message(text=f"You have anothing planned for this year")
        if time_tier == 2: #for month, return name and day
            name_day_result = collection.find({"month": event_month}, {"name":1, "day":1,"_id":0})
            if name_day_result:
                for event_name_list in name_day_result:
                    dispatcher.utter_message(text=f"On the {list(event_name_list.values())[1]}, you have {list(event_name_list.values())[0]}\n")
            else:
                dispatcher.utter_message(text=f"You have anothing planned for this month")
        if time_tier == 3: #for day, return name and time
            name_time_result = collection.find({"day": event_day}, {"name":1, "time":1, "_id":0}) 
            if name_time_result:
                for event_name_list in name_time_result:
                    dispatcher.utter_message(text=f"At {list(event_name_list.values())[1]}, you have {list(event_name_list.values())[0]}\n")
            else:
                dispatcher.utter_message(text=f"You have anothing planned for this day")
        if time_tier == 4: #for time, return just name
            name_result = collection.find({"time": event_time}, {"name":1, "_id":0})
            if name_result:
                for event_name_list in name_result:
                    dispatcher.utter_message(text=f"At {event_time}, you have {list(event_name_list.values())[0]}\n")
            else:
                dispatcher.utter_message(text=f"You have anothing planned for this time")
        if time_tier == 5: #not sure
            name_result = collection.find_one({"name": event_name}, {"name":1, "_id":0})
        if time_tier == 6: #not sure
            name_result = collection.find_one({"location": event_location}, {"name":1, "_id":0}) 

        #SlotSet("event_name", result)
        #reset slots in the conversation
        SlotSet("event_year", value=0.0)
        SlotSet("event_month", 0.0)
        SlotSet("event_day", 0.0)
        SlotSet("event_time", "")
        SlotSet("event_location", "")
        SlotSet("event_name_ent", "")

        #reset slots in the tracker action endpoint
    
        return [SlotSet("event_year", 0.0), SlotSet("event_month", 0.0), SlotSet("event_day", 0.0), 
                SlotSet("event_time", ""), SlotSet("event_location", ""), SlotSet("event_name_ent", "")]
    

class ActionInsertEvent(Action):
    def name(self) -> Text:
        return "ActionInsertEvent"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
        client = MongoClient('mongodb+srv://kevinyin:Anbo%400104@cluster0.4fz5pbg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

        #db=client.test_database

        collection = client['Personal']['events']
        
        event_ins = {
            "name": tracker.get_slot("event_name_ent"),
            "year": tracker.get_slot("event_year"),
            "month": tracker.get_slot("event_month"),
            "day": tracker.get_slot("event_day"),
            "location": tracker.get_slot("event_location"),
            "time": tracker.get_slot("event_time"),
        }

        #events = db.events
        #event_id=events.insert_one(event1_ins).inserted_id
        collection.insert_one(event_ins)
        dispatcher.utter_message("I have added the event to your schedule")
        
        return []

