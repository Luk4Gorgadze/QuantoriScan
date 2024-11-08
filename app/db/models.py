from datetime import datetime, timezone

from sqlalchemy import (Column, DateTime, Enum, ForeignKey, Integer, String,
                        Text)
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.db.enums import FileStatus, FileType


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    files = relationship("File", back_populates="user")
    comments = relationship("Comment", back_populates="user")


class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    file_type = Column(Enum(FileType), nullable=False)
    valid_invalid = Column(Enum(FileStatus), default=FileStatus.valid)
    user_id = Column(Integer, ForeignKey("users.id"))
    size = Column(Integer, nullable=False)
    csv_rows = Column(Integer, nullable=True)
    upload_date = Column(DateTime, default=datetime.now(timezone.utc))

    user = relationship("User", back_populates="files")

    comments = relationship("Comment", back_populates="file")

    def __repr__(self):
        return (f"<File(id={self.id}, title={self.title}, file_type={self.file_type}, "
                f"valid_invalid={self.valid_invalid}, size={self.size}, "
                f"csv_rows={self.csv_rows}, upload_date={self.upload_date}, user_id={self.user_id})>")


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    file_id = Column(Integer, ForeignKey("files.id"))

    user = relationship("User", back_populates="comments")

    file = relationship("File", back_populates="comments")

    def __repr__(self):
        return f"<Comment(id={self.id}, text={self.text}, user_id={self.user_id}, file_id={self.file_id})>"
