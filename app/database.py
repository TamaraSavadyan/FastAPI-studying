# ORM - Object Relational Mapper
# It's used to interact with database through pure Python without SQL 
# Instead of sending requests to database itself
# Also it gives another level of abstraction to one's code

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database-name>'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:154326@localhost/FastAPI' # need to provide URL to the database

# sqlalchemy should have an engine to interact with database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Defines session (сеанс)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Defining base class (like I used in main.py file)
Base = declarative_base()

# All this code above is standard and will work with any project
# This code comes from FastAPI website tutorial

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()