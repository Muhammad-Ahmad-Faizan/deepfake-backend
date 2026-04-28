"""
Database initialization script
Creates default admin user if it doesn't exist in MongoDB
"""
from app.database import get_db
from app.models import User, UserRole
from app.auth import get_password_hash
from app.config import settings
import logging

logger = logging.getLogger(__name__)

def init_db():
    """Initialize database with default admin user"""
    try:
        db = get_db()
        if not db:
            logger.warning("⚠️  Database not connected yet")
            return
        
        # Check if admin exists by email or username
        admin = db.users.find_one({
            "$or": [
                {"email": settings.ADMIN_EMAIL},
                {"username": "admin"}
            ]
        })
        
        if not admin:
            # Create default admin
            admin_user = User(
                email=settings.ADMIN_EMAIL,
                username="admin",
                hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
                role=UserRole.ADMIN,
                is_active=True
            )
            db.users.insert_one(admin_user.to_dict())
            print(f"✅ Admin user created: {settings.ADMIN_EMAIL}")
            print(f"   Password: {settings.ADMIN_PASSWORD}")
        else:
            print(f"ℹ️  Admin user already exists: {admin['email']}")
    
    except Exception as e:
        logger.error(f"❌ Error initializing database: {e}")
        raise

if __name__ == "__main__":
    print("🔧 Initializing database...")
    init_db()
    print("✅ Database initialized successfully!")
