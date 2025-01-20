from sqlmodel import Session,select
from . import models ,schemas
from fastapi import HTTPException,status
from passlib.context import CryptContext
from datetime import date
from ..dependencies import verify_password

def get_user_by_email(db:Session,email:str):
    db_user=db.exec(select(models.Member).where(models.Member.email==email)).first()
    return db_user

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def create_user(db:Session,user:schemas.MemberCreate):
    hashed_password=pwd_context.hash(user.hashed_password)
    db_user=models.Member(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        avatar=user.avatar,
        birthday=user.birthday
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def update_user(db:Session,user:schemas.MemberUpdate,db_user:models.Member):
    if user.name:
        db_user.name=user.name
    if user.email:
        db_user.email=user.email
    if user.avatar:
        db_user.avatar=user.avatar
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_admin(db:Session,user:schemas.MemberUpdateAdmin,db_user:models.Member):
    if user.name:
        db_user.name=user.name
    if user.email:
        db_user.email=user.email
    if user.avatar:
        db_user.avatar=user.avatar
    if user.points:
        db_user.points=user.points
    if user.achievements:
        db_user.achievements=user.achievements
    if user.trend:
        db_user.trend=user.trend
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db:Session,email:str,admin_email:str|None=None,admin_psw:str|None=None):
    db_user=get_user_by_email(db,email)
    if(db_user is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="email not found")
    elif (admin_email and admin_psw):
        admin_user=get_user_by_email(db,admin_email)
        if(admin_user is None):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="admin email not found")
        elif(not verify_password(admin_psw,admin_user.hashed_password)):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="incorrect admin password")
        
        else:
            db.delete(db_user)
            db.commit()
            return db_user
        


