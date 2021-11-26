from app.database import Base
from fastapi.testclient import TestClient
from app.database import get_db
from app.main import app
import pytest
from .database import engine, TestingSessionLocal


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