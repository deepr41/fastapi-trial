
import pytest
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    assert len(res.json()) == len(test_posts)
    def validate_posts_out(post):
        return schemas.PostOut(**post)
    posts_list = list(map(validate_posts_out, res.json()))
    assert res.status_code == 200

def test_unauthorized_user_get_all_posts(client):
    res = client.get('/posts/')
    assert res.status_code == 401

def test_unauthorized_user_get_one_post(client):
    res = client.get(f'/posts/')
    assert res.status_code == 401

def test_unauthorized_user_get_one_post_invalid_id(client):
    res = client.get(f'/posts/500')
    assert res.status_code == 401

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    # print(res.json())
    assert res.status_code == 200
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title
    assert post.Post.published == test_posts[0].published
    assert post.Post.created_at == test_posts[0].created_at
    assert post.Post.owner.id == test_posts[0].owner.id

@pytest.mark.parametrize("title, content, published", [
    ("awesome title", "awesome content", True),
    ("Driving Car", "Driving  a bus", False),
    ])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title":title, "content": content, "published":published})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner.id == test_user['id']


def test_unauthorized_user_delete_post(client):
    res = client.delete("/posts/1")
    assert res.status_code == 401

def test_authorized_user_delete_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_authorized_user_delete_nonexisting_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/100")
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[2].id}")
    assert res.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }

    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)

    created_post = schemas.Post(**res.json())

    assert res.status_code == 200

    assert created_post.title == "updated title"
    assert created_post.content == "updated content"
    assert created_post.published == test_posts[0].published
    assert created_post.owner.id == test_user['id']

def test_update_other_users_post(authorized_client, test_user, test_posts, test_user2):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[2].id
    }

    res = authorized_client.put(f"/posts/{test_posts[2].id}", json=data)

    assert res.status_code == 401

def test_unauthorized_user_update_post(client):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": "1"
    }
    res = client.put("/posts/1", json=data)
    assert res.status_code == 401

def test_authorized_user_update_nonexisting_post(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[2].id
    }
    res = authorized_client.put(f"/posts/100", json=data)
    assert res.status_code == 404