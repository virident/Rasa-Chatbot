from pymongo import MongoClient

client = MongoClient('mongodb+srv://kevinyin:Anbo%400104@cluster0.4fz5pbg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

db=client.test_database

collection = client['Personal']['events']

# event1 = {
#     "name": "fishing",
#     "year": 2024,
#     "month": "July",
#     "day": 11,
#     "location": "fishing pond",
# }

# events = db.events
# event_id=events.insert_one(event1).inserted_id
# collection.insert_one(event1)
# print(db.list_collection_names())

result = collection.find({"month": "July"}, {"name":1, "day":1, "_id":0})
for row in result:
    print("on the", list(row.values())[1], "th you have", list(row.values())[0])