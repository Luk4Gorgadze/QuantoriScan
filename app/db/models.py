from datetime import datetime, timezone
from sqlmodel import Field, Relationship, SQLModel
from app.db.enums import FileStatus, FileType


class User(SQLModel, table=True):
    __tablename__ = "users"  # Define table name

    id: int = Field(primary_key=True, index=True)
    username: str = Field(index=True, nullable=True)
    email: str = Field(unique=True, index=True)
    password: str

    files: list["File"] = Relationship(back_populates="user")
    comments: list["Comment"] = Relationship(back_populates="user")


class File(SQLModel, table=True):
    __tablename__ = 'files'

    id: int = Field(primary_key=True, index=True)
    title: str = Field(index=True)
    file_type: FileType
    valid_invalid: FileStatus = FileStatus.valid
    user_id: int = Field(foreign_key="users.id")
    size: int
    csv_rows: int = 0
    upload_date: datetime = Field(default=datetime.now(timezone.utc))

    user: "User" = Relationship(back_populates="files")
    comments: list["Comment"] = Relationship(back_populates="file")

    def __repr__(self):
        return (f"<File(id={self.id}, title={self.title}, file_type={self.file_type}, "
                f"valid_invalid={self.valid_invalid}, size={self.size}, "
                f"csv_rows={self.csv_rows}, upload_date={self.upload_date}, user_id={self.user_id})>")


class Comment(SQLModel, table=True):
    __tablename__ = 'comments'

    id: int = Field(primary_key=True, index=True)
    text: str
    user_id: int = Field(foreign_key="users.id")
    file_id: int = Field(foreign_key="files.id")

    user: "User" = Relationship(back_populates="comments")
    file: "File" = Relationship(back_populates="comments")

    def __repr__(self):
        return f"<Comment(id={self.id}, text={self.text}, user_id={self.user_id}, file_id={self.file_id})>"
