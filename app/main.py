from fastapi import FastAPI,Depends
from app import models
from app.routers import users,auth,profile,email,pdf
from app.database import engine



app = FastAPI()
# models.Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(email.router)
app.include_router(pdf.router)