from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.db.models as models
from app import auth
from app.auth import get_current_user
from app.db.database import get_db
from app.db.schemas import FileSerializer

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/users/{email}/files", response_model=List[FileSerializer], status_code=status.HTTP_200_OK)
async def get_files_by_user_email(
    email: str,
    user: Annotated[auth.User, Depends(get_current_user)],
    db: db_dependency
) -> List[FileSerializer]:
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    files = db.query(models.File).filter(models.File.user_id == user.id).all()
    return [FileSerializer.model_validate(file) for file in files]
