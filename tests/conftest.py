from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.conf import settings
from app.database import get_db,Base
from alembic import command
import pytest
from app import schema
from jose import jwt

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
engine=create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal= sessionmaker(autocommit=False, autoflush=False,bind=engine)


@pytest.fixture()
def session():
    # to work with alembic 
    # command.upgrade("head")
    # command.downgrade("base")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

# create email and return token
@pytest.fixture
def created_email(client):
    email = {"user_email":"ganesh@gmail.com"}
    res = client.post("/emails/",json=email)
    token = schema.VerifyToken(**res.json())
    assert res.status_code == 201
    return token

# receiving the token from test_email fixture and sending to header
@pytest.fixture
def authorized_client(client,created_email):
    client.headers = {
        **client.headers,"Authorization": created_email.token
    }
    return client

# creating a user
@pytest.fixture
def created_user(authorized_client):
        user_data = {"password":"password"}
        res = authorized_client.post("/users/register",json=user_data)
        new_user = res.json()
        assert res.status_code == 201
        new_user["user_email"] = "ganesh@gmail.com"
        return new_user

# create email and return token
@pytest.fixture
def created_email_2(client):
    email = {"user_email":"vamsi@gmail.com"}
    res = client.post("/emails/",json=email)
    token = schema.VerifyToken(**res.json())
    assert res.status_code == 201
    return token

# receiving the token from test_email fixture and sending to header
@pytest.fixture
def authorized_client_2(client,created_email_2):
    client.headers = {
        **client.headers,"Authorization": created_email_2.token
    }
    return client

# creating a user
@pytest.fixture
def created_user_2(authorized_client_2):
        user_data = {"password":"password"}
        res = authorized_client_2.post("/users/register",json=user_data)
        new_user = res.json()
        assert res.status_code == 201
        new_user["user_email"] = "vamsi@gmail.com"
        return new_user


# creating token for login user
@pytest.fixture
def login_user_token(client,created_user):
    login_data = {"username":"ganesh@gmail.com","password":"password"}
    res = client.post("/login",data=login_data)
    token =schema.Token(**res.json())
    payload = jwt.decode(token.access_token,settings.secret_key,settings.algorithm)
    id:str = payload.get("user_id")
    assert id == created_user["id"]
    assert res.status_code == 201
    return token

# receiving token from login user
@pytest.fixture
def authorized_user(client,login_user_token):
    client.headers["Authorization"]= f"Bearer {login_user_token.access_token}"
    return client

# creating token for user_2 forget password
@pytest.fixture
def user_2_forget_password(client,created_user_2):
    email = {"user_email":created_user_2["user_email"]}
    res = client.post("/users/forget_password",json=email)
    assert res.status_code == 200
    token = schema.VerifyToken(**res.json())
    return token

# receiving token from user_2 forget password
@pytest.fixture
def authorized_user_who_forget_password(client,user_2_forget_password):
    client.headers["Authorization"]= user_2_forget_password.token
    return client

# creating user profile
@pytest.fixture
def create_user_profile(authorized_user):
    data = {"first_name":"ganesh","last_name":"chelluri","date_of_birth":"2000-08-16","phone_number":9876543210,"address":"d/no:-14-115,arilova,visakhapatnam","highest_qualification":"B-tech"}
    res = authorized_user.post("/profile/",json= data)
    assert res.status_code == 201
    new_data = res.json()
    return new_data