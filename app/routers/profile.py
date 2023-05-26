from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from .. import schema,models,oauth2
from app.database import get_db


router = APIRouter(prefix= "/profile",tags= ["Profile"])

#create user profile
@router.post("/", response_model= schema.profileOut, status_code= status.HTTP_201_CREATED)
def create_user_profile(data:schema.profile, db:Session = Depends(get_db), current_user:models.User = Depends(oauth2.get_current_user)):
    # check whether the user profile already exist or not
    profile_data = db.query(models.Profile).filter(models.Profile.user_id == current_user.id).first()
    if profile_data:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "user profile already exits")
    new_data = models.Profile(user_id = current_user.id, **data.dict())
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    # email = db.query(models.Email).join(models.User,models.Email.id == models.User.email_id,isouter=True).filter(models.User.id == new_data.user_id).first()
    # user_mail = email.user_email
    return new_data

# edit user profile
@router.put("/edit_profile", response_model= schema.EditProfileOut)
def edit_profile(data:schema.EditProfile, db:Session = Depends(get_db), current_user:models.User = Depends(oauth2.get_current_user)):
    # check whether the user profile exist or not
    profile_data = db.query(models.Profile).filter(models.Profile.user_id == current_user.id).first()
    if not profile_data:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "Profile not found")
    for field, value in data.dict(exclude_unset = True).items():
        if value is not None:
            setattr(profile_data, field, value)
    db.commit()
    return profile_data
