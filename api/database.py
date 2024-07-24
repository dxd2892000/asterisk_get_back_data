from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL connection URL format
DATABASE_USER = "duc"
DATABASE_PASSWORD = "C7_b9L*EorVBpWLI"
DATABASE_HOST = "192.168.0.39"
DATABASE_NAME = "api_get_back"

SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declare a base class for declarative class definitions
Base = declarative_base()