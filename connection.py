from pymongo import MongoClient
import certifi


# MongoDB connection
client = MongoClient("mongodb+srv://aabdullahbscs20seecs:Multiscan17sf9@cluster0.1kzng0x.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db = client["logoAI"]
collection = db["logos"]
