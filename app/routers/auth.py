from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models,schema,utils,oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(tags= ["Authentication"])

# user login
@router.post("/login", status_code= status.HTTP_201_CREATED, response_model= schema.Token)
def user_login(login_data:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
     # check the email if already in user table or not
    user = db.query(models.User).join(models.Email, models.Email.id == models.User.email_id, isouter=True).filter(models.Email.user_email == login_data.username).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"user with {login_data.username} not found")
    user.is_logged_in = True
    db.commit()
    # check the password
    if not utils.verify(login_data.password, user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "INVALID CREDENTIALS")
    access_token = oauth2.create_access_token(data= {"user_id":user.id})
    return {"access_token":access_token, "token_type":"Bearer"}





