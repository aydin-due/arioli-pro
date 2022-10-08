from pymongo import MongoClient
import certifi

MONGO_URI = 'mongodb+srv://si:si123@arioli-pro.hhjbux9.mongodb.net/?retryWrites=true&w=majority'
ca = certifi.where()

def dbConnection():
    try:
        client = MongoClient(MONGO_URI, tlsCAFile=ca)
        db = client['arioli-pro']
    except ConnectionError:
        print('Error connecting to database')
    return db