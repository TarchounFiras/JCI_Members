from fastapi import APIRouter,HTTPException,status,Security
from typing import Annotated
from database import cruduser ,schemas
from dependencies import session_dep,get_and_verif_token,TokenData
from database.memberList import list_members

router=APIRouter()


@router.get("/list_members",response_model=list[schemas.MemberPublic])
def get_all_members(session:session_dep,token:Annotated[TokenData,Security(get_and_verif_token,scopes=["admin","user"])]):
    members=list_members(session)
    return members

@router.get("/admin/member_profile",response_model=schemas.MemberPublicAdmin)
def get_full_member_profile(session:session_dep,token:Annotated[TokenData,Security(get_and_verif_token,scopes=["admin","user"])],email:str):
    if token.email==email:
        user=cruduser.get_user_by_email(session,email)
    elif "admin" in token.scopes:
        user = cruduser.get_user_by_email(session, email)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="you are not allowed to see this profile with full details")
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found")
    return user

@router.get("/user/member_profile",response_model=schemas.MemberPublic)
def get_member_profile(session:session_dep,token:Annotated[TokenData,Security(get_and_verif_token,scopes=["user"])]):
    user=cruduser.get_user_by_email(session,token.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found")
    return user