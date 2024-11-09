from typing import List

from fastapi import APIRouter, HTTPException, status

import app.db.models as models
from app import auth
from app.db.database import db_dependency
from app.db.schemas import FileSerializer

router = APIRouter()


@router.get("/users/{email}", response_model=List[FileSerializer], status_code=status.HTTP_200_OK)
async def get_files_by_user_email(
    email: str,
    user: auth.user_dependency,
    db: db_dependency
) -> List[FileSerializer]:
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    files = db.query(models.File).filter(models.File.user_id == user.id).all()
    return [FileSerializer.model_validate(file) for file in files]
