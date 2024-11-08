from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app import auth
from app.auth import get_current_user
from app.celery_worker import celery
from app.db.database import get_db
from app.tasks import handle_csv_task, handle_text_task

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/upload/", status_code=status.HTTP_202_ACCEPTED)
async def upload_file(
    user: Annotated[auth.User, Depends(get_current_user)],
    db: db_dependency,
    file: UploadFile = File(...)
) -> dict:
    if file.content_type not in ["text/csv", "text/plain"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid file type. Only CSV and Text files are allowed.")

    file_contents = await file.read()
    file_size = len(file_contents)

    if file.content_type == "text/csv":
        task = handle_csv_task.delay(file_contents=file_contents, user_id=user.id,
                                     file_size=file_size, file_name=file.filename)

    elif file.content_type == "text/plain":
        task = handle_text_task.delay(file_contents=file_contents, user_id=user.id,
                                      file_size=file_size, file_name=file.filename)

    return {"task_id": task.id}


@router.get("/tasks/{task_id}/status", status_code=status.HTTP_200_OK)
async def get_task_status(task_id: str) -> dict:
    task_result = celery.AsyncResult(task_id)
    return {"task_id": task_id, "status": task_result.status, "result": task_result.result}
