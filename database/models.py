from typing import List
from sqlmodel import Field ,Relationship,SQLModel
from datetime import date


class Member(SQLModel, table=True):
    id:int=Field(primary=True)
    name:str=Field()
    birthday:date|None=Field(default=None)
    email:str=Field(unique=True,index=True)
    hashed_password:str=Field()
    points:int=Field(default=0)
    avatar:str|None=Field(default=None)
    achievements:List[str]=Field(default=[])
    trend:str=Field(default="stable")

    
    

