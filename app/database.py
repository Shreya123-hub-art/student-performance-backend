from pymongo import MongoClient

# Connect to MongoDB (local)
client = MongoClient("mongodb://localhost:27017/")

db = client["student_db"]
collection = db["predictions"]