from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,  # Test connections before using
    connect_args={"connect_timeout": 10}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def connect_to_db():
    """Initialize database connection and create tables"""
    try:
        # Test connection
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Connected to PostgreSQL and created tables")
    except Exception as e:
        logger.warning(f"⚠️  Database connection warning: {e}")
        logger.warning("App will continue but database operations may fail")

def close_db():
    """Close database connection"""
    engine.dispose()
    logger.info("Closed PostgreSQL connection")
