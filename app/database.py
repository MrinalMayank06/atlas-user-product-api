from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection string
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

# Create MongoDB client
try:
    client = MongoClient(MONGO_URL)
    # Test connection
    client.admin.command('ping')
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    raise

# Select database
db = client["atlas_user_product_db"]

# Define collections
users_collection = db["users"]
products_collection = db["products"]

# Create indexes for better performance
users_collection.create_index("email", unique=True)
products_collection.create_index("sku", unique=True)