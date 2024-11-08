from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from app.routers import comments, files, upload

import app.auth as auth
import app.db.models as models
from app.db.database import Session, engine, get_db

app = FastAPI()
app.include_router(auth.router)
app.include_router(upload.router, prefix="/upload", tags=["upload"])
app.include_router(comments.router, prefix="/comments", tags=["comments"])
app.include_router(files.router, prefix="/files", tags=["files"])

models.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(get_db)]


@app.get('/', status_code=status.HTTP_200_OK)
async def user(user: Annotated[auth.User, Depends(auth.get_current_user)], db: db_dependency) -> dict:
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    return {"User": user}
