from fastapi import APIRouter , Depends , HTTPException , Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db
from ..models import User
from ..schema import login, Token
from sqlalchemy.orm import Session
from .. import utils , oauth2

routers = APIRouter(tags=['Authetication'])

@routers.post("/login", response_model=Token)
def login(loginInfo: OAuth2PasswordRequestForm = Depends() , db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == loginInfo.username).first()
    if not user:
        raise HTTPException(status_code=403, detail="No user with this email!")
        
    verify = utils.verify(loginInfo.password, user.password)

    if not verify:
        raise HTTPException(status_code=403, detail="password invalid!")

    token = oauth2.create_access_token(data={"user_id" : user.id})

    return {"access_token" : token, "token_type" : "bearer"}
    
