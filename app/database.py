
import pymongo


class Singleton:
    _instances = None

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]


class MongoConnection(metaclass=Singleton):
    def __init__(self):
        self.host = 'mongodb://localhost:27017'

    def __enter__(self):
        self.client = pymongo.MongoClient(self.host)
        self.db = self.client['book-db']
        self.book_collection = self.db['books']
        self.user_collection = self.db['users']
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.client.close()