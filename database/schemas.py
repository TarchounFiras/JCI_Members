from pydantic import BaseModel
from datetime import date

class MemberPublic(BaseModel):
    name:str
    email:str
    points:int
    avatar:str|None=None
    achievements:list[str]
    trend:str

class MemberPublicAdmin(MemberPublic):
    birthday:date|None=None
    
class MemberCreate(BaseModel):
    name:str
    email:str
    avatar:str|None=None
    birthday:date|None=None
    hashed_password:str


class MemberUpdate(BaseModel):
    name:str|None=None
    email:str|None=None
    avatar:str|None=None

class MemberUpdateAdmin(MemberUpdate):
    points:int|None=None
    achievements:list[str]|None=None
    trend:str|None=None
