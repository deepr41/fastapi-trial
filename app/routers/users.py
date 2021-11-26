from pydantic import utils
from .. import models, schemas, utils, oauth2
from fastapi.param_functions import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm.session import Session
from fastapi import status
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

# create user
@router.post('/',response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate,db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# get user
@router.get('/{id}',response_model=schemas.UserOut)
async def get_user(id : int, db: Session = Depends(get_db), 
        get_current_user:int = Depends(oauth2.get_current_user)):
    new_user = db.query(models.User).filter(models.User.id == id).first()
    return new_user

