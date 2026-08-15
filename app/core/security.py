from datetime import datetime,timedelta,timezone
import bcrypt
from jose import jwt
from app.core.config import SECRET_KEY,ACCESS_TOKEN_EXPIRE_MINUTES
def hash_password(p): return bcrypt.hashpw(p.encode(),bcrypt.gensalt()).decode()
def verify_password(p,h): return bcrypt.checkpw(p.encode(),h.encode())
def token(uid): return jwt.encode({"sub":str(uid),"exp":datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)},SECRET_KEY,algorithm="HS256")
