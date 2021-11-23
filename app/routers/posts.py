from typing import List, Optional
from fastapi import Response, status
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.routing import APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm.session import Session


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# get posts
@router.get('/',response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db), 
        current_user:int = Depends(oauth2.get_current_user),
        limit:int = 10, skip:int = 0, search:Optional[str] = ""):

    posts = db.query(models.Post).filter(models.Post.title.contains(search)).offset(skip).limit(limit).all()
    return posts

# get post by id
@router.get('/{id}',response_model=schemas.Post)
async def get_post(id:int, db: Session = Depends(get_db), 
        current_user:int = Depends(oauth2.get_current_user)): #enforces the type
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id: {id} was not found")
    return post

# update post by id
@router.put('/{id}', response_model=schemas.Post)
async def update_post(id:int, new_post:schemas.PostCreate, db: Session = Depends(get_db), 
        current_user:int = Depends(oauth2.get_current_user)): #enforces the type
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id: {id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Not authorized to perform this action")

    post_query.update(new_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()

# create post
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_posts(post:schemas.PostCreate, db: Session = Depends(get_db), 
        current_user:int = Depends(oauth2.get_current_user)):
    
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# delete post by id
@router.delete('/{id}')
async def get_posts(id:int, db: Session = Depends(get_db), 
        current_user:int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id: {id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Not authorized to perform this action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)