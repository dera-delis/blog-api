from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

# Monkey patch to fix passlib/bcrypt compatibility issue
# The wrap bug detection uses a 200-byte test string that exceeds bcrypt's 72-byte limit
import bcrypt as _bcrypt

# Store original hashpw
_original_bcrypt_hashpw = _bcrypt.hashpw

def _patched_bcrypt_hashpw(secret, salt):
    """Patched bcrypt.hashpw that truncates secrets longer than 72 bytes."""
    if isinstance(secret, bytes) and len(secret) > 72:
        secret = secret[:72]
    return _original_bcrypt_hashpw(secret, salt)

# Apply the patch
_bcrypt.hashpw = _patched_bcrypt_hashpw

# Also patch passlib's detect_wrap_bug to catch any remaining errors (if it exists)
try:
    import passlib.handlers.bcrypt as bcrypt_module
    
    if hasattr(bcrypt_module, 'detect_wrap_bug'):
        _original_detect_wrap_bug = bcrypt_module.detect_wrap_bug
        
        def _patched_detect_wrap_bug(ident):
            """Patched version that handles 72-byte limit gracefully."""
            try:
                return _original_detect_wrap_bug(ident)
            except ValueError as e:
                # If the test fails due to 72-byte limit, assume no wrap bug
                if "cannot be longer than 72 bytes" in str(e):
                    return False
                raise
        
        bcrypt_module.detect_wrap_bug = _patched_detect_wrap_bug
except (ImportError, AttributeError):
    # If detect_wrap_bug doesn't exist or can't be patched, that's okay
    # The bcrypt.hashpw patch should be sufficient
    pass

from passlib.context import CryptContext

from app.config import settings
from app.database import get_db
from app.models import User
from app.schemas import TokenData

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_v1_str}/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """Authenticate a user with username and password."""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """Get the current authenticated user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Get the current active user."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
