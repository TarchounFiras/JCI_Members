from fastapi import APIRouter,Depends,HTTPException,status
from typing import Annotated
from ..database import cruduser ,schemas
from datetime import timedelta
from ..dependencies import session_dep,authenticate_user,ACCESS_TOKEN_EXPIRE_HOURS,create_access_token,get_and_verif_token,OAuth2PasswordRequestForm,Token,TokenData
from fastapi.security import Security
from ..database.memberList import list_members

router=APIRouter()


@router.get("/list_members",response_model=list[schemas.MemberPublic])
def get_all_members(session:session_dep,token:Annotated[TokenData,Security(get_and_verif_token,scopes=["admin","user"])]):
    members=list_members(session)
    return members

@router.get("/member_profile",response_model=list[schemas.MemberPublicAdmin])
def get_member_profile(session:session_dep,token:Annotated[TokenData,Security(get_and_verif_token,scopes=["admin","user"])],email:str):
    if token.email==email:
        user=cruduser.get_user_by_email(session,email)
    elif "admin" in token.scopes:
        user = cruduser.get_user_by_email(session, email)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="you are not allowed to see this profile full details")
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found")
    return user

