from ..database import get_db
from sqlalchemy.orm import Session
from ..schema import CreateUser , userResponse
from fastapi import HTTPException , Depends, APIRouter
from .. import models
from .. import utils

router = APIRouter(prefix="/users" , tags=['Users'])


@router.post("/", status_code=201, response_model=userResponse)
def createUser(user : CreateUser,db : Session = Depends(get_db)):
    hashedpss = utils.hash(user.password)
    user.password = hashedpss

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}", response_model=userResponse)
def getUser(id:int , db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="no user with this id")

    return user