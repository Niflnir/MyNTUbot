import json
import os
from pymongo import MongoClient

f = open("./mongoschemas/CEE.json")
document = json.load(f)
print(document)
client = MongoClient(os.environ.get("MONGODB"))
db = client["ntubot"]
collection = db["courseandyear"]
for i in document:
    collection.insert_one(i)
