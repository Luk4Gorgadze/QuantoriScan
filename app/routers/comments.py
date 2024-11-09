from typing import List

from fastapi import APIRouter, HTTPException, status

import app.db.models as models
from app import auth
from app.db.database import db_dependency
from app.db.schemas import CommentCreate, CommentSerializer

router = APIRouter()


@router.post("/files/{file_id}", status_code=status.HTTP_201_CREATED)
async def add_comment(
    file_id: int,
    comment_data: CommentCreate,
    user: auth.user_dependency,
    db: db_dependency
) -> dict:
    file = db.query(models.File).filter(models.File.id == file_id).first()  # type: ignore
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    new_comment = models.Comment(
        text=comment_data.text,
        user_id=user.id,
        file_id=file_id
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return {"message": "Comment added successfully", "comment_id": new_comment.id}


@router.get("/files/{file_id}", response_model=List[CommentSerializer], status_code=status.HTTP_200_OK)
async def get_comments_for_file(
    file_id: int,
    user: auth.user_dependency,
    db: db_dependency
) -> List[CommentSerializer]:
    file = db.query(models.File).filter(models.File.id == file_id).first()  # type: ignore
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    comments = db.query(models.Comment).filter(models.Comment.file_id == file_id).all()  # type: ignore

    if not comments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No comments found for this file")

    return [CommentSerializer.model_validate(comment) for comment in comments]
