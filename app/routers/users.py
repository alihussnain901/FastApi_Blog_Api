from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session 
from ..database import get_db
from .. import models, schemas, utils

router = APIRouter(
    prefix="/users",
    tags=["Users"]  
)

# Create User
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.Users, db: Session = Depends(get_db)):

    # Check if user already exists by email
    existing_user = db.query(models.Users).filter(models.Users.email == user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User already exists with this email"
        )

    # Hash the password before storing it
    hashed_password = utils.get_password_hash(user.password)

    # Prepare new user data
    user_data = user.model_dump() 
    user_data["password"] = hashed_password

    new_user = models.Users(**user_data)

    # Save to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# Get Users List
@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.Users).all()
    return users

# Get One User
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="user does not exits")
    return user

# Delete User
@router.delete("/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id)
    if user.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="user does not exits")
    user.delete(synchronize_session=False)
    db.commit()
    return {"user deleted successfully"}