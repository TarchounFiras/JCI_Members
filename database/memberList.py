from sqlmodel import Session , select
from sqlalchemy import desc
from . import models
from .cruduser import get_user_by_email


def list_members(db:Session):
    members=db.exec(select(models.Member).order_by(desc(models.Member.points), desc(models.Member.presence))).all()
    res=list(members)
    for i  in range(len(res)):
        if res[i].rank<i+1:
            db_user=get_user_by_email(db,res[i].email)
            db_user.rank=i+1
            db_user.trend="down"
            db.commit()
            db.refresh(db_user)
        elif res[i].rank>i+1:
            db_user=get_user_by_email(db,res[i].email)
            db_user.rank=i+1
            db_user.trend="up"
            db.commit()
            db.refresh(db_user)
        else:
            db_user=get_user_by_email(db,res[i].email)
            db_user.trend="stable"
            db.commit()
            db.refresh(db_user)
        
        
    return res



