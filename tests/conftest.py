from app.database import Base
from fastapi.testclient import TestClient
from app.database import get_db
from app.main import app
import pytest
from .database import engine, TestingSessionLocal
from app import oauth2, models
import copy


@pytest.fixture()
def session():
    ### Clearing out the test database
    #drops all the tables in the databases
    Base.metadata.drop_all(bind = engine)

    #creates all the tables in the databases
    Base.metadata.create_all(bind = engine)

    # # With Alembic
    # command.downgrade("base")
    # command.upgrade("head")

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

@pytest.fixture()
def test_user(client):
    user_data = {"email":"deep@gmail.com",
                 "password":"password123"}
    res = client.post("/users/",json=user_data)
    assert res.status_code == 201
    new_user = res.json() 
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture()
def test_user2(client):
    user_data = {"email":"deep1@gmail.com",
                 "password":"password123"}
    res = client.post("/users/",json=user_data)
    assert res.status_code == 201
    new_user = res.json() 
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture()
def token(test_user):
    access_token = oauth2.create_access_token(data = {"user_id": test_user['id']})
    return access_token

@pytest.fixture()
def authorized_client(client, token):
    # auth_client = copy.deepcopy(client)
    auth_client = client
    auth_client.headers = {
        **client.headers,
        "Authorization":f"bearer {token}"
    }
    return auth_client

@pytest.fixture()
def test_posts(authorized_client, test_user, session, test_user2):
    posts_data = [
        {"title": "first post", "content" : "first content", "owner_id" : test_user['id']},
        {"title": "second post", "content" : "second content", "owner_id" : test_user['id']},
        {"title": "third post", "content" : "third content", "owner_id" : test_user2['id']},
        ]
    
    def create_post_model(post):
        return models.Post(**post)

    posts_models = list(map(create_post_model, posts_data))

    session.add_all(posts_models)
    session.commit()

    return session.query(models.Post).all()
