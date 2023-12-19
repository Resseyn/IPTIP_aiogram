from pymongo import MongoClient

from data.configs import mongo_host

# создайте экземпляр клиента MongoClient
client = MongoClient(mongo_host)

# получите базу данных из клиента
mongo_db = client["comics_db_bot"]
mongo_comics = mongo_db["comics"]
