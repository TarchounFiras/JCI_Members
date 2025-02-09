from sqlmodel import Session,select

from database import models ,schemas
from fastapi import HTTPException,status
from passlib.context import CryptContext
from dependencies import verify_password,vacuum_database

def get_user_by_email(db:Session,email:str):
    db_user=db.exec(select(models.Member).where(models.Member.email==email)).first()
    return db_user

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def create_user(db:Session,user:schemas.MemberCreate):
    db_user=get_user_by_email(db,user.email)
    if (db_user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="email already registered")
    else:    
        hashed_password=pwd_context.hash(user.password)
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

def update_user(db:Session,user:schemas.MemberUpdate,email:str,old_password:str|None=None):
    db_user=get_user_by_email(db,email)
    if user.name:
        db_user.name=user.name

    if user.email:
        db_user.email=user.email

    if user.avatar:
        db_user.avatar=user.avatar

    if user.password and old_password:
        if verify_password(old_password,db_user.hashed_password):
            db_user.hashed_password=pwd_context.hash(user.password)
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="incorrect password")
                
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_admin(db:Session,user:schemas.MemberUpdateAdmin,email:str,admin_email:str|None=None,admin_pwd:str|None=None):
    db_user=get_user_by_email(db,email)
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

    if user.presence:
        db_user.presence=user.presence

    if user.password:
        if not admin_email or not admin_pwd:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Admin credentials required to change password"
            )
        
        db_admin = get_user_by_email(db, admin_email)
        if not db_admin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Admin email not found"
            )
        
        if not verify_password(admin_pwd, db_admin.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect admin password"
            )
    
        db_user.hashed_password = pwd_context.hash(user.password)
    
    
    db.commit()
    db.refresh(db_user)
    return db_user

delete_counter=0
def delete_user(db:Session,email:str,admin_email,admin_pwd:str):
    db_user=get_user_by_email(db,email)
    if(db_user is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="email not found")
    elif (admin_email and admin_pwd):
        admin_user=get_user_by_email(db,admin_email)
        if(admin_user is None):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="admin email not found")
        elif(not verify_password(admin_pwd,admin_user.hashed_password)):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="incorrect admin password")
        
        else:
            global delete_counter
            delete_counter+=1
            if delete_counter>=50:
                vacuum_database()
                delete_counter=0

            db.delete(db_user)
            db.commit()  
            return {email:"deleted"}
        

    

        


