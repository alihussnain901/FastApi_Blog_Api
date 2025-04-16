from fastapi import FastAPI
from database import engine
import models
from routers import users, posts, auth, votes


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(posts.router)    
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/")
def read_root():
    return {"Hello": "Welcome to Fastapi"}



@app.get("/shawaiz")
def shezy():
    
    return {"Name": "Shawaiz",
            "Age": 23,
            "City": "Gujranwala",
            "Country": "Pakistan",
            "Occupation": "DevOps Engineer",
            "Hobby": "Coding"}





