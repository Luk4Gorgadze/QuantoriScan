import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.security import (HTTPAuthorizationCredentials, HTTPBearer,
                              OAuth2PasswordBearer)
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status

from app.db.database import db_dependency
from app.db.models import User
from app.db.schemas import Token

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)

security = HTTPBearer()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, email: EmailStr = Form(...), password: str = Form(...)):
    try:
        create_user_model = User(
            email=email,
            password=bcrypt_context.hash(password),
        )
        db.add(create_user_model)
        db.commit()
        return {"message": "User created successfully"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post('/token', response_model=Token)
async def login_for_access_token(db: db_dependency,  email: EmailStr = Form(...), password: str = Form(...)):
    user = authenticate_user(email, password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    token = create_access_token(user.email, user.id, timedelta(minutes=120))

    return {"access_token": token, "token_type": "bearer"}


def authenticate_user(username_email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == username_email).first()  # type: ignore
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user


def create_access_token(email: str, user_id: int, expires_delta: timedelta):
    encode = {
        "sub": email,
        "user_id": user_id,
    }
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(db: db_dependency, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = db.query(User).filter(User.email == payload.get("sub")).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

user_dependency = Annotated[User, Depends(get_current_user)]
