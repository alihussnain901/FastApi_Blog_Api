from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils, oauth2
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])

@router.post("/login")
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Check if user exists in the database
    db_user = db.query(models.Users).filter(models.Users.email == user.username).first()
    
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # Verify the password
    if not utils.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # Create a token for the user
    access_token = oauth2.create_access_token(data={"user_id": str(db_user.id)})
    
    return {"message": "access token created", "access_token": access_token, "token_type": "bearer"}
