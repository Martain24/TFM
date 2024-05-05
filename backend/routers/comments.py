from .. import models, schemas, database
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Tuple
from .. import utils
import pandas as pd

router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)

@router.get("/", response_model=List[schemas.CommentOutput])
def get_comments(limit:int = 10, db:Session = Depends(database.get_db)):
    comments = db.query(models.Comments).order_by(func.random()).limit(limit).all()
    return comments

@router.post("/", response_model=schemas.CommentOutput)
def create_comment(new_comment:schemas.CommentInput, db:Session = Depends(database.get_db),
                    current_user=Depends(utils.get_current_user)):
    new_comment = new_comment.model_dump()
    new_comment["user_id"] = current_user.id
    new_comment = models.Comments(**new_comment)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment
