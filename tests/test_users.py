import pytest
from app import schemas
from jose import jwt
from app.config import settings


def test_create_user(client):
    res = client.post("/users/", json={"email":"deepak4567@gmail.com", "password":"password123"})
    #using pydantic to test output to conform to the schema
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "deepak4567@gmail.com"
    assert res.status_code == 201


def test_login_user(client,test_user):
    res = client.post("/login", data={"username":test_user['email'], "password":test_user['password']})
    assert res.status_code == 200

    login_res =  schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id:str = payload.get("user_id")
    assert login_res.token_type == "bearer"
    assert id == test_user['id']

@pytest.mark.parametrize("email, password, status_code",[
    ("wrongemail@gmail.com", 'password123', 403),
    ("deepak@gmail.com", 'wrongpassword', 403),
    ("wrongemail@gmail.com", 'wrongpassword', 403),
    (None, 'password123', 422),
    ("deepak@gmail.com", None, 422),
    ])
def test_incorrent_login(test_user,client, email, password, status_code):
    res = client.post('/login', data={"username":email, "password":password})

    assert res.status_code == status_code
    # assert res.json()['detail'] == "Invalid Credentials"