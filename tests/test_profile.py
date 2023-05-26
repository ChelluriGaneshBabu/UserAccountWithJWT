# authorized user creating user profile
def test_authorized_user_create_user_profile(authorized_user):
    data = {"first_name":"ganesh","last_name":"chelluri","date_of_birth":"2000-08-16","phone_number":9876543210,"address":"d/no:-14-115,arilova,visakhapatnam","highest_qualification":"B-tech"}
    res = authorized_user.post("/profile/",json= data)
    assert res.status_code == 201

# unauthorized user creating user profile
def test_unauthorized_user_create_user_profile(client,created_user):
    data = {"first_name":"ganesh","last_name":"chelluri","date_of_birth":"2000-08-16","phone_number":9876543210,"address":"d/no:-14-115,arilova,visakhapatnam","highest_qualification":"B-tech"}
    res = client.post("/profile/",json= data)
    assert res.status_code == 401

# authorized user creating profile again
def test_authorized_user_create_user_profile_again(authorized_user,create_user_profile):
    data = {"first_name":"ganesh","last_name":"chelluri","date_of_birth":"2000-08-16","phone_number":9876543210,"address":"d/no:-14-115,arilova,visakhapatnam","highest_qualification":"B-tech"}
    res = authorized_user.post("/profile/",json= data)
    assert res.status_code == 403

# authorized user editing profile
def test_authorized_user_edit_profile(authorized_user,create_user_profile):
    data = {"first_name":"ganesh babu","phone_number":9640734595}
    res = authorized_user.put("/profile/edit_profile",json= data)
    assert res.status_code == 200

# unauthorized user editing profile
def test_authorized_user_edit_profile(client,create_user_profile):
    client.headers["Authorization"]="None"
    data = {"first_name":"ganesh babu","phone_number":9640734595}
    res = client.put("/profile/edit_profile",json= data)
    assert res.status_code == 401

# authorized user editing profile which not exist
def test_authorized_user_edit_profile_not_exist(authorized_user):
    data = {"first_name":"ganesh babu","phone_number":9640734595}
    res = authorized_user.put("/profile/edit_profile",json= data)
    assert res.status_code == 404