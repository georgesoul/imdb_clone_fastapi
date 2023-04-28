from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from typing import Optional, List
from sqlalchemy.orm import Session
from .. import util
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get('/', response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db), 
                    current_user: schemas.UserOut = Depends(oauth2.get_current_user),
                    limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute(""" SELECT * FROM posts; """)
    # posts = cursor.fetchall()
    
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), 
                      current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

@router.get('/{id}', response_model=schemas.Post)
async def get_post(id: int, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, str(id))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")
    return post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, str(id))
    # deleted_post = cursor.fetchone()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform this action")
        
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemas.Post)
async def update_post(id: int, post: schemas.PostUpdate, 
                      db: Session = Depends(get_db), 
                      current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, 
    #                (post.title, post.content, post.published, str(id)))
    
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")
        
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform this action")
    
    updated_post = post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()