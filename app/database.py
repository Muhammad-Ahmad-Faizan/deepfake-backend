from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# MongoDB connection
client = None
db = None

def connect_to_mongo():
    global client, db
    try:
        client = MongoClient(settings.DATABASE_URL, serverSelectionTimeoutMS=5000)
        # Test connection
        client.admin.command('ping')
        db = client.deepfake_db  # Database name
        logger.info("✅ Connected to MongoDB")
        
        # Create indexes
        create_indexes()
    except ConnectionFailure as e:
        logger.error(f"❌ Failed to connect to MongoDB: {e}")
        raise

def close_mongo():
    global client
    if client:
        client.close()
        logger.info("Closed MongoDB connection")

def create_indexes():
    """Create necessary indexes"""
    if db:
        # Users collection
        db.users.create_index("email", unique=True)
        db.users.create_index("username", unique=True)
        
        # Videos collection
        db.videos.create_index("user_id")
        db.videos.create_index("uploaded_at")
        db.videos.create_index("status")

def get_db():
    """Dependency to get database instance"""
    return db
