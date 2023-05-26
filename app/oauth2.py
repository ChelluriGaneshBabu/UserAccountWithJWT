from datetime import datetime,timedelta
from jose import JWTError,jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status,Response
from sqlalchemy.orm import Session
from app import database,schema,models
from .conf import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl= 'login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_time

# Creating access token
def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)
    return encoded_jwt

def verify_token(token:str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        # to get user_id from payload which is in dict form
        id :str = payload.get("user_id")
        # to send id to schema
        token_data = schema.TokenData(id = id)
    except JWTError:
        raise  HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "could not validate credentials or Invalid token", headers= {"WWW_Authenticate":"Bearer"})
    return token_data

def get_current_user(response: Response, token:str = Depends(oauth2_schema), db:Session = Depends(database.get_db)):
    # verify the token
    token_data = verify_token(token)
    # create a new token to change the expire time
    created_token = renew_access_token(token)
    # sending the new token back to header in response
    response.headers.append("new_token", created_token)
    # check the user present in user table or not
    user = db.query(models.User).filter(models.User.id == token_data.id,models.User.is_logged_in == True).first()
    if not user:
            raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "user was not logged in")
    return user

def verify_token_expire(token:str):
    try:
        decoded_jwt = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        
    except JWTError:
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "could not validate credentials or Invalid token", headers= {"WWW_Authenticate":"Bearer"})
    return decoded_jwt


# Function to automatically renew access token if it is about to expire
def renew_access_token(encoded_jwt: str):
    # decode the token to check the expire time
    decoded_jwt = verify_token_expire(encoded_jwt)
    if decoded_jwt is None:
        # Token is invalid or has expired
        return None
    now = datetime.now()    # current time
    expire_time = datetime.fromtimestamp(decoded_jwt["exp"])   # by using fromtimestamp it convert GMT time to normal time
    remaining_time = expire_time - now
    if remaining_time.total_seconds() < (ACCESS_TOKEN_EXPIRE_MINUTES * 60) / 2:
        # Token is about to expire, so renew it
        new_data = decoded_jwt.copy()
        new_data.pop("exp", None)
        return create_access_token(data= {"user_id":new_data["user_id"]})
    else:
        # Token is still valid, so no need to renew it
        return encoded_jwt

