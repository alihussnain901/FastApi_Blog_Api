from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/votes",
    tags=["Votes"],
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(vote: schemas.Vote, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == user_id.id)

    found_vote = vote_query.first()

    if (vote.dir == 1):
        if found_vote:
         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="already voted")
        
        new_vote = models.Votes(post_id=vote.post_id, user_id=user_id.id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {"message": "Vote created successfully"}
    
    else:
       if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
       vote_query.delete(synchronize_session=False)
       db.commit()
       return {"message": "Vote deleted successfully"}
    
 