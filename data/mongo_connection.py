import pymongo
from pymongo import MongoClient

#connecting to default local mongodb://localhost:27017/
client = MongoClient()



def getconnection2collection(databse:str,collection:str):
    try:
        db = client[databse]
        collection = db[collection]
        collection.client = client
        return collection
    except Exception as e:
        print("error connecting mongo database",e)