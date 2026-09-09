
from ..database import get_db
from sqlalchemy.orm import Session
from ..schema import StudentResponse , UpdateStudent , Student, StudentVote
from fastapi import HTTPException , Depends, APIRouter
from .. import models , oauth2
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(prefix="/student" , tags=['Students'])

@router.post("/" , status_code=201 , response_model=StudentResponse)
def create_stu(stu:Student , db:Session = Depends(get_db) , user_id : int = Depends(oauth2.get_current_user)):
    
    new_stu = models.Student(user_id = user_id.id ,**stu.dict())
    db.add(new_stu)
    db.commit()
    db.refresh(new_stu)
    return new_stu

@router.get("/", response_model=List[StudentVote])
def all_stu(
    db: Session = Depends(get_db),
    user_id: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""
):

    students = (
        db.query(
            models.Student,
            func.count(models.Votes.stu_id).label("votes")
        )
        .outerjoin(
            models.Votes,
            models.Student.id == models.Votes.stu_id
        )
        .filter(
            models.Student.name.contains(search)
        )
        .group_by(models.Student.id)
        .limit(limit)
        .offset(skip)
        .all()
    )

    return [
            {
                "student": student,
                "votes": votes
            }
        for student, votes in students
    ]

@router.get("/{id}", response_model=StudentVote)
def get_stu(id:int , db:Session = Depends(get_db), user_id : int = Depends(oauth2.get_current_user)):
    stud =  (
        db.query(
            models.Student,
            func.count(models.Votes.stu_id).label("votes")
        )
        .outerjoin(
            models.Votes,
            models.Student.id == models.Votes.stu_id
        ).filter(
             models.Student.id == id).group_by(models.Student.id).first()
        )
    
    if stud == None:
        raise HTTPException(status_code=404 , detail="No student with this id")

    student, votes = stud
    
    return {
                    "student": student,
                    "votes": votes
                }
            
        


@router.put("/{id}", response_model=StudentResponse)
def update_stu(id : int , stu : UpdateStudent , db : Session = Depends(get_db), user_id : int = Depends(oauth2.get_current_user)):
    data = stu.model_dump(exclude_none=True)

    if not data:
        raise HTTPException(status_code=400, detail="No field provided")

    stud = db.query(models.Student).filter(models.Student.id == id).first()

    if stud == None:
        raise HTTPException(status_code=404, detail="No student with this id")

    
    if stud.user_id != user_id.id:
            raise HTTPException(status_code=403 , detail="You are not authorized to update this!")

    for i , j in data.items():
        setattr(stud,i,j) 

    db.commit()
    db.refresh(stud)

    return stud
    
@router.delete("/{id}", response_model=StudentResponse) 
def delete_stu(id : int, db : Session = Depends(get_db), user_id : int = Depends(oauth2.get_current_user)):
    Stu = db.query(models.Student).filter(models.Student.id == id).first()
    if Stu == None:
        raise HTTPException(status_code=404 , detail="No student with this id")

    if Stu.user_id != user_id.id:
            raise HTTPException(status_code=403 , detail="You are not authorized to delete this!")

    Stu.user
    
    db.delete(Stu)
    db.commit()
    return Stu

