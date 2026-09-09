from fastapi import Depends, APIRouter , HTTPException
from ..database import get_db
from ..oauth2 import get_current_user
from ..schema import Vote
from .. import models
from sqlalchemy.orm import Session

router = APIRouter(prefix="/vote" , tags=['Vote'])

@router.post("/", status_code=201)
def vote(
    votes: Vote,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    
    Stu = db.query(models.Student).filter(
        models.Student.id == votes.stu_id).first()

    if not Stu:
        raise HTTPException(status_code=404, detail="No such stu_post exist")
    
    vote_query = db.query(models.Votes).filter(
            models.Votes.stu_id == votes.stu_id,
            models.Votes.user_id == current_user.id
        ).first()
    

    if votes.dir == 1:

        if vote_query:
            raise HTTPException(
                status_code=409,
                detail="This user has already voted"
            )

        new_vote = models.Votes(
            stu_id=votes.stu_id,
            user_id=current_user.id
        )

        db.add(new_vote)
        db.commit()

        return {"message": "Successfully voted"}

    if votes.dir == 0:

        if not vote_query:
            raise HTTPException(
                status_code=404,
                detail="No vote found from this user"
            )

        db.delete(vote_query)
        db.commit()

        return {"message": "Vote removed successfully"}

