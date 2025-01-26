from pydantic import BaseModel
from datetime import date

class MemberPublic(BaseModel):
    name:str
    email:str
    avatar:str|None=None
    points:int
    presence:int
    achievements:str
    trend:str
    rank:int
    joining_year:int



class MemberPublicAdmin(MemberPublic):
    birthday:date|None=None
    
class MemberCreate(BaseModel):
    name:str
    email:str
    avatar:str|None=None
    birthday:date|None=None
    password:str
    joining_year:int|None=None


class MemberUpdate(BaseModel):
    name:str|None=None
    email:str|None=None
    avatar:str|None=None
    password:str|None=None

class MemberUpdateAdmin(MemberUpdate):
    points:int|None=None
    achievements:str|None=None
    joining_year:int|None=None
    presence:int|None=None
