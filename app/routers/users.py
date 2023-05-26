from fastapi import APIRouter,Depends,status,HTTPException,Header,Response
from sqlalchemy.orm import Session
from app import schema,models,oauth2,utils
from app.database import get_db
from datetime import datetime


router = APIRouter(prefix= "/users",tags= ["Users"])

# verify token and register
@router.post("/register", status_code = status.HTTP_201_CREATED, response_model = schema.UserOut)
def create_user(response:Response,user_data:schema.User_create, Authorization:str = Header(...), db:Session = Depends(get_db)):
    # check the token
    if Authorization == "None":
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "user already registerd")
    # verify the token from header
    token_data = oauth2.verify_token(Authorization)
    verified_user = db.query(models.Email).filter(models.Email.id == token_data.id).first()
    if not verified_user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail= "no email found")
     # override the verified token with none value after register in postman environment variable
    response.headers.append("token","None")
    # convert the user plain_password to hashed password
    hashed_password = utils.hash(user_data.password)
    user_data.password = hashed_password
    new_user = models.User(email_id = verified_user.id, **user_data.dict())
    db.add(new_user)
    db.commit()
    # to get the data after commiting to database
    db.refresh(new_user)
    return new_user


# change to new password
@router.put("/change_password", status_code= status.HTTP_200_OK)
def change_password(passwords_data:schema.ChangePassword, db:Session = Depends(get_db), current_user:models.User = Depends(oauth2.get_current_user)):
    # verify the password
    if not utils.verify(passwords_data.old_password, current_user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Incorrect password")
    hashed_password = utils.hash(passwords_data.new_password)
    current_user.password = hashed_password
    current_user.modified_on = datetime.now()
    db.commit()
    return {"message":"password changed successfully"}

#forget password
@router.post("/forget_password", response_model= schema.VerifyToken, status_code= status.HTTP_200_OK)
def forget_password(email:schema.EmailIn, db:Session = Depends(get_db)):
    user = db.query(models.User).join(models.Email, models.User.email_id == models.Email.id).filter(models.Email.user_email == email.user_email).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"user {email.user_email} not found")
    token = oauth2.create_access_token(data= {"user_id":user.id})
    return {"token":token, "token_type":"Bearer"}

#set new password
@router.put("/set_new_password", status_code= status.HTTP_200_OK)
def set_new_password(password:schema.SetNewPassword, Authorization= Header(...), db:Session=Depends(get_db)):
    # verify the token 
    token_data = oauth2.verify_token(Authorization)
    verified_user = db.query(models.User).filter(models.User.email_id == token_data.id).first()
    if not verified_user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail= "no email found")
    hashed_password = utils.hash(password.new_password)
    verified_user.password = hashed_password
    verified_user.modified_on = datetime.now()
    db.commit()
    return {"message":"password set successfully"}

#user logout
@router.put("/logout", status_code= status.HTTP_200_OK)
def user_logout(db:Session = Depends(get_db), current_user:models.User = Depends(oauth2.get_current_user)):
    email =db.query(models.Email).join(models.User, models.Email.id == models.User.email_id, isouter=True).filter(current_user.email_id == models.Email.id).first()
    current_user.is_logged_in = False
    db.commit()
    return {"message":f"User {email.user_email} was successfully logged out"}


