from fastapi import APIRouter,Depends,HTTPException,status,Security
from typing import Annotated
from ..database import cruduser ,schemas
from datetime import timedelta
from ..dependencies import session_dep,authenticate_user,ACCESS_TOKEN_EXPIRE_HOURS,create_access_token,get_and_verif_token,OAuth2PasswordRequestForm,Token,TokenData


router=APIRouter()

#**** SIGN UP CREATE USER
@router.post("/admin/sign_up",status_code=status.HTTP_201_CREATED)
#async def create_newuser(newuser:schemas.MemberCreate,session:session_dep,token:Annotated[TokenData,Security(get_and_verif_token,scopes=["admin"])]):
async def create_newuser(newuser:schemas.MemberCreate,session:session_dep):   
    user=cruduser.create_user(session,newuser)
    if(user):
        return {"user creation":"successful"}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

#***Login
@router.post("/token",description="LOGIN:you can give the email instead of the username")
async def login_for_access_token(session:session_dep,form_data:Annotated[OAuth2PasswordRequestForm,Depends()]):
    
    user=authenticate_user(session,form_data.username,form_data.password)
    if(not user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires=timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    access_token=create_access_token(data={"sub":user.email,"scopes":form_data.scopes},expires_delta=access_token_expires)

    

    return Token(access_token=access_token,token_type="bearer")







# **** UPDATE USER  (Admin)***
@router.put("/admin/update_user_info",response_model=schemas.MemberPublicAdmin,description=" update presence and points + user details ,   IMPORTANT : both admin  and user roles are required")
async def update_user_admin(session:session_dep,token:Annotated[TokenData,Security(get_and_verif_token,scopes=["admin","user"])],updated_user:schemas.MemberUpdateAdmin,useremail:str,admin_pwd:str|None=None):
    user=cruduser.update_user_admin(session,updated_user,useremail,token.email,admin_pwd)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user



# **** UPDATE USER  (user)***
@router.put("/user/update_user_info",response_model=schemas.MemberPublic,description=" update user details ,   IMPORTANT : user role is required")
async def update_user(session:session_dep,token:Annotated[TokenData,Security(get_and_verif_token,scopes=["user"])],updated_user:schemas.MemberUpdate,old_password:str|None=None):
    user=cruduser.update_user_admin(session,updated_user,token.email,old_password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user




# **** DELETE USER ***
@router.delete("/admin/delete_user",status_code=status.HTTP_200_OK,description=" ,   IMPORTANT : both admin  and user roles are required")
async def delete_user(session:session_dep,token:Annotated[TokenData,Security(get_and_verif_token,scopes=["admin","user"])],member_email:str,admin_password:str):
    return cruduser.delete_user(session,member_email,token.email,admin_password)

