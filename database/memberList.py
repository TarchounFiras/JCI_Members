from sqlmodel import Session , select
from sqlalchemy import desc
from . import models
from .cruduser import get_user_by_email
from fastapi import HTTPException,status


def list_members(db:Session):
    members=db.exec(select(models.Member).order_by(desc(models.Member.points))).all()
    res=list(members)
    for i  in range(len(res)):
        if res[i].rank<i:
            res[i].rank=i+1
            res[i].trend="up"
        elif res[i].rank>i:
            res[i].rank=i+1
            res[i].trend="down"
        db.add(res[i])
        
    db.commit()
    return res


def member_profile(db:Session,email:str):
    member=get_user_by_email(db,email)
    if (member):
        return member
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="member not found")

