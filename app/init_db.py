"""
Database initialization script
Creates default admin user if it doesn't exist
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import User, UserRole
from app.auth import get_password_hash
from app.config import settings

def init_db():
    """Initialize database with tables and default admin"""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if admin exists by email or username
        admin = db.query(User).filter(
            (User.email == settings.ADMIN_EMAIL) | (User.username == "admin")
        ).first()
        
        if not admin:
            # Create default admin
            admin = User(
                email=settings.ADMIN_EMAIL,
                username="admin",
                hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
                role=UserRole.ADMIN,
                is_active=True
            )
            db.add(admin)
            db.commit()
            print(f"✅ Admin user created: {settings.ADMIN_EMAIL}")
            print(f"   Password: {settings.ADMIN_PASSWORD}")
        else:
            print(f"ℹ️  Admin user already exists: {admin.email}")
    
    finally:
        db.close()

if __name__ == "__main__":
    print("🔧 Initializing database...")
    init_db()
    print("✅ Database initialized successfully!")
