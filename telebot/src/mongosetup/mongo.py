import os
from pymongo import MongoClient


def mongo(collectionName):
    client = MongoClient(os.environ.get("MONGODB"))
    db = client["ntubot"]
    collection = db[collectionName]
    return collection
