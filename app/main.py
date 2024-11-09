from fastapi import FastAPI, HTTPException, status

import app.auth as auth
from app.db.database import db_dependency
from app.db.schemas import UserResponse
from app.routers import comments, files, upload

app = FastAPI()
app.include_router(auth.router)
app.include_router(upload.router, prefix="/upload", tags=["upload"])
app.include_router(comments.router, prefix="/comments", tags=["comments"])
app.include_router(files.router, prefix="/files", tags=["files"])


@app.get('/', status_code=status.HTTP_200_OK)
async def user(user: auth.user_dependency, db: db_dependency) -> UserResponse:
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    return UserResponse.model_validate(user)
