from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.db.enums import FileStatus, FileType


class FileSerializer(BaseModel):
    id: int
    title: str
    file_type: FileType
    size: int
    valid_invalid: FileStatus
    upload_date: datetime
    csv_rows: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class CommentCreate(BaseModel):
    text: str


class CommentSerializer(BaseModel):
    id: int
    text: str
    user_id: int
    file_id: int

    model_config = ConfigDict(from_attributes=True)
