from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, LargeBinary, BigInteger
from sqlalchemy.orm import sessionmaker, Session

# Database setup
DATABASE_URL = "postgresql://postgres:Postgres%40123@localhost/postgres"

# The line Base = declarative_base() is part of the SQLAlchemy library and is used to create a base class for all the models (database tables) in an application.
Base = declarative_base()

# User Model (Admin and Candidate)
class User(Base):
    __tablename__ = 'users1'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)  # 'admin' or 'candidate'
    
# Database connection setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creatting A Table With all the columns.
Base.metadata.create_all(bind=engine)