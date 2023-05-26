
# authorized user generating pdf
def test_authorized_user_generate_profile_pdf(authorized_user,create_user_profile):
    res = authorized_user.get("/profile_pdf")
    assert res.status_code == 201

# unauthorized user generating pdf
def test_unauthorized_user_generate_profile_pdf(client,create_user_profile):
    client.headers["Authorization"]="None"
    res = client.get("/profile_pdf")
    assert res.status_code == 401

# authorized user generating pdf which not exist
def test_authorized_user_generate_profile_pdf_not_exist(authorized_user):
    res = authorized_user.get("/profile_pdf")
    assert res.status_code == 404
