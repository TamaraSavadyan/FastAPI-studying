from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, models, utils, oauth2
from ..database import get_db

router = APIRouter(
    tags=['Authentication']
)



@router.post('/login', response_model=schemas.Token)
# def login(user_credentials: schemas.UserLogin, ...):
# using this built-in FastAPI class "OAuth2PasswordRequestForm" is more convienient 
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):    
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")

    # Checking provided password with hashed password from database
    # To do that we need to hash provided password and compare with hashed password from database
    # Because hash-function is a one-way encryption
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")

    # create a token (JWT token authentication)
    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    return {"access_token": access_token, 
            "token_type": "bearer"}