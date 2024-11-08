from typing import Dict

from sqlalchemy.orm import Session

from app.celery_worker import celery
from app.db.database import SessionLocal
from app.logic.file_handlers import handle_csv, handle_text


@celery.task(name='handle_csv_task')
def handle_csv_task(file_contents: bytes, user_id: int, file_size: int, file_name: str) -> Dict[str, str]:
    db: Session = SessionLocal()
    try:
        uploaded: bool = handle_csv(file_contents, db, file_name, file_size, user_id)
        if uploaded:
            return {"status": "success", "message": "CSV file is valid and saved successfully"}
        return {"status": "failed", "message": "CSV file is invalid and processing failed"}
    finally:
        db.close()


@celery.task(name="handle_text_task")
def handle_text_task(file_contents: bytes, user_id: int, file_size: int, file_name: str) -> Dict[str, str]:
    db: Session = SessionLocal()
    try:
        uploaded: bool = handle_text(file_contents, db, file_name, file_size, user_id)
        if uploaded:
            return {"status": "success", "message": "Text file is valid and saved successfully"}
        return {"status": "failed", "message": "Text file is invalid and processing failed"}
    finally:
        db.close()
