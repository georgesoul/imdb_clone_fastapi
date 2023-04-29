from fastapi import FastAPI
from app import models
# from app.database import engine
from app.routes import user, post, auth, vote
from fastapi.middleware.cors import CORSMiddleware

# Initialize our db based on our sqlalchemy models - deactivated since we introduced alembic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "*"
    # "https://www.google.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
        
@app.get('/')
def root():
    return {"message": "It works!"}