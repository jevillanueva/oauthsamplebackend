from app import configuration
import pymongo
client  = pymongo.MongoClient(configuration.MONGO_URI)
db = client.get_database(configuration.MONGO_DB)