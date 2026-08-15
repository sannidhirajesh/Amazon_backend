import os
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL=os.getenv("DATABASE_URL","postgresql+psycopg://postgres:postgres@db:5432/amazon_db")
SECRET_KEY=os.getenv("SECRET_KEY","dev-secret")
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES","60"))
