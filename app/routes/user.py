from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import util
from ..models import User
from ..schemas import UserCreate, UserOut
from ..database import get_db

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    
    hashed_password = util.hash(user.password)
    user.password = hashed_password
    
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.get('/{id}', response_model=UserOut)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} does not exist")
    return user