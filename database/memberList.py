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
            db_user=get_user_by_email(db,res[i].email)
            db_user.rank=i+1
            db_user.trend="up"
        elif res[i].rank>i:
            db_user.rank=i+1
            db_user.trend="down"
        db.commit()
        db.refresh(db_user)
        
    db.commit()
    db.refresh()
    return res



