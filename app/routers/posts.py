from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_active_user
from app.crud import (
    get_posts, get_post, create_post, update_post, delete_post, get_user_posts
)
from app.schemas import Post, PostCreate, PostUpdate
from app.models import User

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=List[Post])
def read_posts(
    skip: int = 0,
    limit: int = 100,
    published_only: bool = False,
    db: Session = Depends(get_db)
):
    """Get all posts with pagination."""
    posts = get_posts(db, skip=skip, limit=limit, published_only=published_only)
    return posts


@router.get("/{post_id}", response_model=Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    """Get a specific post by ID."""
    db_post = get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
def create_new_post(
    post: PostCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new post."""
    return create_post(db=db, post=post, user_id=current_user.id)


@router.put("/{post_id}", response_model=Post)
def update_post_info(
    post_id: int,
    post_update: PostUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update post information (only own posts)."""
    db_post = get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if db_post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    updated_post = update_post(db, post_id=post_id, post_update=post_update)
    return updated_post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_by_id(
    post_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a post (only own posts)."""
    db_post = get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if db_post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    success = delete_post(db, post_id=post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
    return None


@router.get("/user/{user_id}", response_model=List[Post])
def read_user_posts(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all posts by a specific user."""
    posts = get_user_posts(db, user_id=user_id, skip=skip, limit=limit)
    return posts


@router.get("/my/posts", response_model=List[Post])
def read_my_posts(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user's posts."""
    posts = get_user_posts(db, user_id=current_user.id, skip=skip, limit=limit)
    return posts
