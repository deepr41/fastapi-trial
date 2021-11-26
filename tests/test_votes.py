import pytest
from app import models

@pytest.fixture()
def vote_on_post(session, test_posts,test_user):
    new_vote = models.Vote(post_id = test_posts[2].id, owner_id=test_user['id'])
    session.add(new_vote)
    session.commit()

def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post("/vote", json = {"post_id":test_posts[0].id, "dir":True})
    assert res.status_code == 201

def test_vote_twice_on_post(authorized_client, test_posts, vote_on_post):
    res = authorized_client.post("/vote", json = {"post_id":test_posts[2].id, "dir":True})
    assert res.status_code == 409

def test_delete_vote_on_post(authorized_client, test_posts, vote_on_post):
    res = authorized_client.post("/vote", json = {"post_id":test_posts[2].id, "dir":False})
    assert res.status_code == 204

def test_delete_on_unvoted_post(authorized_client, test_posts):
    res = authorized_client.post("/vote", json = {"post_id":test_posts[2].id, "dir":False})
    assert res.status_code == 404

def test_vote_non_exists(authorized_client, test_posts):
    res = authorized_client.post("/vote", json = {"post_id":200, "dir":False})
    assert res.status_code == 404

def test_vote_unauthorized_user(client):
    res = client.post("/vote", json = {"post_id":200, "dir":False})
    assert res.status_code == 401