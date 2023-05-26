
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# converting the password to hash password
def hash(password:str):
    return pwd_context.hash(password)

# Verifying the login user password with hashed password in database
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
