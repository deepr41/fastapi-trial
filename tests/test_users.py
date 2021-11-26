from .database import client, session
from app import schemas

import pytest

def test_root(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json().get('message') == 'Hello World'

@pytest.mark.parametrize("email, password", [("deepak4567@gmail.com", "password123")])
def test_create_user(client, email, password ):
    res = client.post("/users/", json={"email":email, "password":password})
    #using pydantic to test output to conform to the schema
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == email
    assert res.status_code == 201