from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from app.db.database import SessionLocal
from app.db.models import User

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)

SECRET_KEY = 'SomethingSecret'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CreateUserRequest(BaseModel):
    email: str
    password: str


class EmailPasswordRequest(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = User(
        email=create_user_request.email,
        password=bcrypt_context.hash(create_user_request.password),
    )
    db.add(create_user_model)
    db.commit()


@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: EmailPasswordRequest,
                                 db: db_dependency):
    user = authenticate_user(form_data.email, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    token = create_access_token(user.email, user.id, timedelta(minutes=120))

    return {"access_token": token, "token_type": "bearer"}


def authenticate_user(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
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


async def get_current_user(db: db_dependency, token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = db.query(User).filter(User.email == payload.get("sub")).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


# if someone wants to pass token in header, left it here on purpose xd
# async def get_current_user(db: db_dependency, token: Annotated[str, Header(alias="Authorization")]):
#     try:
#         if not token.startswith("Bearer "):
#             raise HTTPException(status_code=403, detail="Invalid authentication scheme")
#         token_value = token.split("Bearer ")[1]
#         payload = jwt.decode(token_value, SECRET_KEY, algorithms=[ALGORITHM])
#         user = db.query(User).filter(User.email == payload.get("sub")).first()
#         if user is None:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
#         return user
#     except JWTError:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
