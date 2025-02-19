from fastapi import APIRouter, status, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from db.session import get_db
from db.models.user import User
from apis.v1.route_login import get_current_user
from schemas.blog import CreateBlog, ShowBlog, UpdateBlog
from db.repository.blog import create_new_blog, retrieve_blog, list_blogs, update_blog_by_id, delete_blog_by_id

router = APIRouter()

@router.post("/", response_model=ShowBlog, status_code=status.HTTP_201_CREATED)
def create_blog(blog : CreateBlog, db : Session = Depends(get_db),current_user : User = Depends(get_current_user)):
    print(f"Authenticated user: {current_user.email}")  # Debug print
    blog = create_new_blog(blog=blog, db=db, author_id = current_user.id)
    return blog

@router.get("/{id}", response_model=ShowBlog)
def get_blog(id : int, db : Session = Depends(get_db)):
    blog = retrieve_blog(id = id, db = db)
    if not blog:
        raise HTTPException(detail=f"Blog with ID : {id} does not exist", status_code=status.HTTP_404_NOT_FOUND)
    return blog

@router.get("", response_model=List[ShowBlog])
def get_all_blogs(db : Session = Depends(get_db)):
    blog = list_blogs(db = db)
    if not blog:
        raise HTTPException(detail="Currently no blogs are available.", status_code=status.HTTP_204_NO_CONTENT)
    return blog

@router.put("/{id}", response_model=ShowBlog)
def update_a_blog(id: int, blog : UpdateBlog, db : Session = Depends(get_db), current_user : User = Depends(get_current_user)):
    blog = update_blog_by_id(id = id, blog = blog, db = db, author_id = current_user.id)
    if isinstance(blog,dict):
        raise HTTPException(
            detail=blog.get("error"),
            status_code=status.HTTP_400_BAD_REQUEST
        )
    return blog

@router.delete("/{id}")
def delete_a_blog(id: int, db : Session = Depends(get_db), current_user : User = Depends(get_current_user)):
    message = delete_blog_by_id(id = id, db = db, author_id = current_user.id)
    if message.get("error"):
        raise HTTPException(detail=message.get("error"), status_code=status.HTTP_400_BAD_REQUEST)
    return {"msg": message.get("msg")}