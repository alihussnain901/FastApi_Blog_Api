from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, oauth2
from sqlalchemy import func     

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# Create Post
@router.post("/")
def create_post(post: schemas.Posts, db: Session = Depends(get_db), user_id : int = Depends(oauth2.get_current_user)):
    new_post = models.Posts(**post.model_dump())
    owner_id = user_id.id
    new_post.owner_id = owner_id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"post created successfully"}

# Get All Posts
@router.get('/', response_model=list[schemas.PostResponse])

def get_posts(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user),
              limit: int = 3, skip: int = 0, search: str = ""):
    
    post_query = db.query(models.Posts, func.count(models.Votes.post_id).label("votes"))\
        .outerjoin(models.Votes, models.Posts.id == models.Votes.post_id)\
        .group_by(models.Posts.id).filter(models.Posts.title.contains(search))\
        .group_by(models.Posts.id).limit(limit).offset(skip)
    
    post = post_query.all()

    post_responses = []
    for post, votes in post:
        post_responses.append(schemas.PostResponse(
            title=post.title,
            content=post.content,
            publish=post.publish,
            id=post.id,
            owner_id=post.owner_id,
            owner=post.owner,  
            votes=votes
        ))

    return post_responses
    
# Get One Post
@router.get('/{id}', response_model=schemas.PostResponse)

def get_posts_by_id(id: int, db: Session = Depends(get_db)):
    
    post_with_votes = db.query(models.Posts, func.count(models.Votes.post_id).label("votes"))\
        .outerjoin(models.Votes, models.Posts.id == models.Votes.post_id)\
        .group_by(models.Posts.id)\
        .filter(models.Posts.id == id)\
        .first()

    if post_with_votes is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post does not exist")

    post, votes = post_with_votes

    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "owner_id": post.owner_id,
        "owner": post.owner,
        "votes": votes
    }

# Update Post
@router.put("/{id}")
def update_post(post: schemas.Posts, id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    existing_post = post_query.first()
    if existing_post.owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="not authorized to perform requested action")
    if existing_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="post does not exits")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return {"post updated successfully"}

# Delete Post
@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="post does not exits")
    if post.owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="not authorized to perform requested action")

    post = db.query(models.Posts).filter(models.Posts.owner_id == user_id.id)
    post.delete(synchronize_session=False)
    db.commit()
    return {"post deleted successfully"}
