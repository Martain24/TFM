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
    if db.query(models.Predictions).filter(models.Predictions.id == new_comment.prediction_id).first() == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Yo cannot comment on a prediction that does not exist")
    new_comment = new_comment.model_dump()
    new_comment["user_id"] = current_user.id
    new_comment = models.Comments(**new_comment)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@router.delete("/")
def delete_comment(id_comment: int, db: Session = Depends(database.get_db),
                   current_user=Depends(utils.get_current_user)):
    #USUARIOS VIP PUEDEN ELIMINAR CUALQUIER COMENTARIO
    if current_user.is_vip:
        comment_to_delete = db.query(models.Comments).filter(models.Comments.id == id_comment).first()
        if comment_to_delete is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"There does not exist a comment with ID {id_comment}.")
        
        db.delete(comment_to_delete)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    #LOS USUARIOS NO VIP SOLO PUEDEN ELIMINAR SUS PROPIOS COMENTARIOS
    comment_to_delete = db.query(models.Comments).filter(models.Comments.id == id_comment)
    if comment_to_delete.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There does not exists a comment with (id = {id_comment}).")
    if comment_to_delete.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You cannot delete a comment that is not yours.")
    
    comment_to_delete.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)