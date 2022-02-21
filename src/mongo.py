import json
import pymongo
import os
from pymongo import MongoClient

f = open("schema.json")
document = json.load(f)
client = MongoClient(os.environ.get("MONGODB"))
db = client["ntubot"]
collection = db["courseandyear"]
for i in document:
    collection.insert_one(i)
