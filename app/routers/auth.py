from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database.models import User,UserRole
from app.schemas.schemas import Register,UserOut,Login
from app.core.security import hash_password,verify_password,token
router=APIRouter()
@router.post("/register",response_model=UserOut,status_code=201)
def register(x:Register,db:Session=Depends(get_db)):
    if db.query(User).filter_by(email=x.email).first(): raise HTTPException(400,"Email already registered")
    u=User(name=x.name,email=x.email,password_hash=hash_password(x.password),phone=x.phone,role=UserRole.CUSTOMER)
    db.add(u); db.commit(); db.refresh(u); return u
@router.post("/login")
def login(x:Login,db:Session=Depends(get_db)):
    u=db.query(User).filter_by(email=x.email).first()
    if not u or not verify_password(x.password,u.password_hash): raise HTTPException(401,"Invalid email or password")
    return {"access_token":token(u.id),"token_type":"bearer","user":UserOut.model_validate(u)}
