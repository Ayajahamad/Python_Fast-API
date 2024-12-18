# # database.py
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from config import DATABASE_URL

# # Database connection setup
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Base for models
# Base = declarative_base()

# # Function to initialize the database (create tables)
# def init_db():
#     Base.metadata.create_all(bind=engine)


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

# Database connection setup (no need for check_same_thread for PostgreSQL)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base for models
Base = declarative_base()

# Function to initialize the database (create tables)
def init_db():
    Base.metadata.create_all(bind=engine)
