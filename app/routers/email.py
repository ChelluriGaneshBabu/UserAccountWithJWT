from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from app import schema,models,oauth2
from app.database import get_db

router = APIRouter(prefix= "/emails",tags= ["EMail"])

# create email and send token
@router.post("/", response_model= schema.VerifyToken, status_code= status.HTTP_201_CREATED)
def create_email(email:schema.EmailIn, db:Session = Depends(get_db)):
    # check the email if already in email table or not
    user = db.query(models.Email).filter(models.Email.user_email == email.user_email).first()
    if not user:
        new_email = models.Email(**email.dict())
        db.add(new_email)
        db.commit()
        db.refresh(new_email)
        token = oauth2.create_access_token(data= {"user_id":new_email.id})
        return {"token":token, "token_type":"Bearer"}
    else:
        user_query = db.query(models.User).filter(models.User.email_id == user.id).first()
        if user_query:
            raise HTTPException(status_code=status.HTTP_226_IM_USED, detail="enter new email")
        token = oauth2.create_access_token(data= {"user_id":user.id})
        return {"token":token, "token_type":"Bearer"}
