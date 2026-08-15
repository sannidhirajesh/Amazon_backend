from fastapi import Depends,HTTPException
from fastapi.security import HTTPBearer
from jose import jwt,JWTError
from sqlalchemy.orm import Session
from app.core.config import SECRET_KEY
from app.database.database import get_db
from app.database.models import User
bearer=HTTPBearer()
def current_user(c=Depends(bearer),db:Session=Depends(get_db)):
    try: uid=int(jwt.decode(c.credentials,SECRET_KEY,algorithms=["HS256"])["sub"])
    except (JWTError,KeyError,ValueError): raise HTTPException(401,"Invalid token")
    u=db.get(User,uid)
    if not u: raise HTTPException(401,"User not found")
    return u
def roles(*allowed):
    def dep(u=Depends(current_user)):
        if u.role not in allowed: raise HTTPException(403,"Insufficient permissions")
        return u
    return dep
