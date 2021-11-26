from fastapi import APIRouter, HTTPException,status
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from starlette.responses import Response
from .. import schemas,models, database, oauth2

router = APIRouter()

@router.post('/vote', status_code=status.HTTP_201_CREATED)
def vote(vote_request:schemas.Vote, db:Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    #check if post with id exists
    post_query = db.query(models.Post).filter(models.Post.id == vote_request.post_id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {vote_request.post_id} was not found")
    
    #check if vote already exists
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote_request.post_id, models.Vote.owner_id == current_user.id)
    vote = vote_query.first()

    if  vote:
        #vote exists
        if vote_request.dir:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with {current_user.id} has already voted on post {vote_request.post_id}")
        else:
            #delete vote
            vote_query.delete(synchronize_session=False)
            db.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        if vote_request.dir:
            new_vote = models.Vote(owner_id = current_user.id, post_id = vote_request.post_id)
            db.add(new_vote)
            db.commit()
            return {"message":"success"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post of {vote_request.post_id} doesn't have a vote from {current_user.id}")