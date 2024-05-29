from .database import MongoConnection
from .models import Book
from bson import ObjectId


async def fetch_all_books():
    with MongoConnection() as mongo:
        books = []
        cursor = mongo.book_collection.find({})
        async for document in cursor:
            books.append(Book(**document))
        return books


async def fetch_book_by_id(id: str):
    with MongoConnection() as mongo:
        document = await mongo.book_collection.find_one({"_id": ObjectId(id)})
        if document:
            return Book(**document)


async def add_book(book_data: dict):
    with MongoConnection() as mongo:
        result = await mongo.book_collection.insert_one(book_data)
        new_book = await fetch_book_by_id(result.inserted_id)
        return new_book


async def update_book(id: str, book_data: dict):
    with MongoConnection() as mongo:
        await mongo.book_collection.update_one({"_id": ObjectId(id)}, {"$set": book_data})
        updated_book = await fetch_book_by_id(id)
        return updated_book


async def delete_book(id: str):
    with MongoConnection() as mongo:
        result = await mongo.book_collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count
