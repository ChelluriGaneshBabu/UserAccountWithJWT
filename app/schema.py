from typing import Optional
from pydantic import BaseModel,EmailStr,constr
from datetime import datetime,date

class EmailIn(BaseModel):
    user_email:EmailStr

class EmailOut(BaseModel):
    id:int
    email:str
    class Config:
        orm_mode=True

class User_create(BaseModel):
      password:str
      modified_on:Optional[datetime]
      is_logged_in:Optional[bool]

class UserOut(BaseModel):
    id:int
    created_at:datetime
    class Config:
        orm_mode=True

class VerifyToken(BaseModel):
    token:str
    token_type:str

class TokenData(BaseModel):
    id:int

class Token(BaseModel):
    access_token:str
    token_type:str

class ChangePassword(BaseModel):
    old_password:str
    new_password:str

class SetNewPassword(BaseModel):
    new_password:str

class profile(BaseModel):
      first_name:str
      last_name:str
      date_of_birth:date
      phone_number: constr(regex=r'^\+?[0-9]{10,12}$')
      address:str
      highest_qualification:str

class profileOut(profile):
    # email:str
    id:int
    user_id:int
    class Config:
        orm_mode=True

class EditProfile(BaseModel):
      first_name:str=None
      last_name:str=None
      date_of_birth:date=None
      phone_number: constr(regex=r'^\+?[0-9]{10,12}$')=None
      address:str=None
      highest_qualification:str=None

class EditProfileOut(profile):
      pass
      class Config:
           orm_mode=True