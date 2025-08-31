from sqlalchemy.orm import Session

from app.auth import get_password_hash
from app.models import Post, User
from app.schemas import PostCreate, PostUpdate, UserCreate, UserUpdate


# User CRUD operations
def get_user(db: Session, user_id: int) -> User:
    """Get user by ID."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User:
    """Get user by email."""
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> User:
    """Get user by username."""
    return db.query(User).filter(User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Get all users with pagination."""
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user."""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email, username=user.username, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> User:
    """Update user information."""
    db_user = get_user(db, user_id)
    if not db_user:
        return None

    update_data = user_update.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    """Delete a user."""
    db_user = get_user(db, user_id)
    if not db_user:
        return False

    db.delete(db_user)
    db.commit()
    return True


# Post CRUD operations
def get_post(db: Session, post_id: int) -> Post:
    """Get post by ID."""
    return db.query(Post).filter(Post.id == post_id).first()


def get_posts(
    db: Session, skip: int = 0, limit: int = 100, published_only: bool = False
):
    """Get all posts with pagination."""
    query = db.query(Post)
    if published_only:
        query = query.filter(Post.published == True)
    return query.offset(skip).limit(limit).all()


def get_user_posts(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """Get posts by user ID."""
    return (
        db.query(Post).filter(Post.author_id == user_id).offset(skip).limit(limit).all()
    )


def create_post(db: Session, post: PostCreate, user_id: int) -> Post:
    """Create a new post."""
    db_post = Post(**post.dict(), author_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update_post(db: Session, post_id: int, post_update: PostUpdate) -> Post:
    """Update post information."""
    db_post = get_post(db, post_id)
    if not db_post:
        return None

    update_data = post_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_post, field, value)

    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post(db: Session, post_id: int) -> bool:
    """Delete a post."""
    db_post = get_post(db, post_id)
    if not db_post:
        return False

    db.delete(db_post)
    db.commit()
    return True
