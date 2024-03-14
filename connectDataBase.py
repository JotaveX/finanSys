from pymongo import MongoClient

class ConnectDataBase:
    def __init__(self, collectionName):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['financys']
        self.collection = self.db[collectionName]

    def insertData(self, data):
        self.collection.insert_one(data)

    def findData(self, data):
        return self.collection.find(data)
    
    def findId(self, data):
        return self.collection.find_one(data)

    def updateData(self, data, newData):
        self.collection.update_one(data, newData)

    def deleteData(self, data):
        self.collection.delete_one(data)

    def deleteAllData(self):
        self.collection.delete_many({})

    def closeConnection(self):
        self.client.close()
    
    def showData(self):
        return self.collection.find()
