from typing import Optional, List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils  # '.' means current directory
from .database import engine, get_db
from .routers import post, user, auth

# credentials = реквизиты для входа (email/password)
# payload = the actual information or message in transmitted data,
#           as opposed to automatically generated metadata.

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# connecting to database
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='FastAPI',
                                user='postgres', password='154326',
                                cursor_factory=RealDictCursor)
        # cursor_factory will give a column name with value
        # (it will return dicitonary "column":"value")
        cursor = conn.cursor()
        print("Database connected")
        break
    except Exception as error:
        print("Connecting to Database failed")
        print("Error: ", error)
        time.sleep(2)

# request comes with Get method and path url: "/smth"


@app.get("/home")
def root():
    return {"message": "Welcome to my API !!!"}


app.include_router(post.router)  # this will import all specific routes
# so we can keep our files simplier
# distinct code operations on user and post
app.include_router(user.router)

app.include_router(auth.router)
