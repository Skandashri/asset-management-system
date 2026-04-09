from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database URL for PostgreSQL
# User should replace user, password, host, port, dbname with their actual credentials
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """ Dependency that provides a database session """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
