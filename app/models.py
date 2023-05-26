from .database import Base
from sqlalchemy import Column,DateTime,Integer,BigInteger,String,ForeignKey,Date,Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class Email(Base):
    __tablename__ = "emails"
    id = Column(Integer,primary_key=True)
    user_email = Column(String,unique=True,nullable=False)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True)
    email_id = Column(Integer,ForeignKey("emails.id",ondelete="CASCADE"),nullable=False)
    password = Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    modified_on=Column(DateTime)
    is_logged_in =Column(Boolean,nullable=False,server_default="False")
   
class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer,primary_key=True)
    first_name = Column(String,nullable=False)
    last_name  = Column(String,nullable=False)
    date_of_birth = Column(Date,nullable=False)
    phone_number=Column(BigInteger,nullable=False)
    address = Column(String,nullable=False)
    highest_qualification = Column(String,nullable=False)
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    