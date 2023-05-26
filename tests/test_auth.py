from app import schema
from jose import jwt
from app.conf import settings
import pytest

# created user tryong to login
def test_user_login(client,created_user):
    login_data = {"username":"ganesh@gmail.com","password":"password"}
    res = client.post("/login",data=login_data)
    token =schema.Token(**res.json())
    payload = jwt.decode(token.access_token,settings.secret_key,settings.algorithm)
    id:str = payload.get("user_id")
    assert id == created_user["id"]
    assert res.status_code == 201

# not a user trying to login
def test_not_a_user_login(client):
    login_data = {"username":"unregistered@gmail.com","password":"password"}
    res = client.post("/login",data = login_data)
    assert res.status_code == 404

# logging with incorrect credentials
@pytest.mark.parametrize("username,password,status_code",[
    ("banu@gmail.com","password",404),
    ("ganesh@gmail.com","wrongpasswrod",403),
    (None,"password",422),
    ("ganesh@gmail.com",None,422)])

def test_incorrect_user_login(client,created_user,username,password,status_code):
    login_data = {"username":username,"password":password}
    res = client.post("/login",data=login_data)
    assert res.status_code == status_code

