from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, LargeBinary, BigInteger
from sqlalchemy.orm import sessionmaker, Session
from database_config import DATABASE_URL


# The line Base = declarative_base() is part of the SQLAlchemy library and is used to create a base class for all the models (database tables) in an application.
Base = declarative_base()

# Creating a Model(Table in Database)
class Employee(Base):
    __tablename__ = "Employee"
    
    id = Column(Integer,primary_key=True)
    e_name = Column(String)
    email = Column(String)
    number = Column(BigInteger)
    qualification = Column(String)
    role = Column(String)
    filename = Column(String)
    file_data = Column(LargeBinary)


# User Model (Admin and Candidate)
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)  # 'admin' or 'candidate'
    

# Database connection setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creatting A Table With all the columns.
Base.metadata.create_all(bind=engine)