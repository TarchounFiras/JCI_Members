
from fastapi import Depends,HTTPException,status,Security
from typing import Annotated
from .database.database import engine
from .database import cruduser
from sqlmodel import Session,select
from datetime import date,timedelta
from datetime import datetime, timedelta,timezone
from passlib.context import CryptContext
from pydantic import BaseModel
import jwt
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from fastapi.security import (OAuth2PasswordBearer , OAuth2PasswordRequestForm , SecurityScopes)



import os
from dotenv import load_dotenv




#***session dependency
def get_session():
    with Session(engine) as session:
        yield session
session_dep=Annotated[Session,Depends(get_session)]



    


#****  LOGIN AND HANDLE JWT TOKEN ***

#to get a secret key (string like this ) type in powershell :-join ((1..32) | ForEach-Object { "{0:x2}" -f (Get-Random -Minimum 0 -Maximum 256) })


load_dotenv() #load env var from .env file

#get the var 
SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_HOURS = 5

oauth2_scheme= OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"admin":"membre bureau can add delete and update normal members","user":"normal member can update his profiel and see memberlist"}
    )



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
    scopes:list[str]=[]


def create_access_token(data:dict ,expires_delta:timedelta|None=None):
    to_encode=data.copy()
    if(expires_delta):
        expire=datetime.now(timezone.utc)+ expires_delta
    else:
        expire=datetime.now(timezone.utc)+timedelta(hours=1)
    
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def authenticate_user(session,email:str,password:str):
    user=cruduser.get_user_by_email(session,email)
    if(not user):
        return False
    if not verify_password(password,user.hashed_password):
        return False
    
    return user




def get_and_verif_token(security_scopes:SecurityScopes,token:Annotated[str,Depends(oauth2_scheme)]):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'

    else:
        authenticate_value = 'Bearer'
    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email=payload.get("sub")
        if email is None:
            raise credentials_exception
        token_scopes=payload.get("scopes",[])
        token_data=TokenData(email=email,scopes=token_scopes)
        for scope in security_scopes.scopes:
            if scope not in token_data.scopes:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not enough permissions",
                    headers={"WWW-Authenticate": authenticate_value},
                )
        
    except (InvalidTokenError,ValidationError):
        raise credentials_exception
    return token_data
