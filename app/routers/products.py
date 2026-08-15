from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database.models import Product,User,UserRole
from app.schemas.schemas import ProductIn
from app.core.dependencies import roles
router=APIRouter()
@router.post("",status_code=201)
def add(x:ProductIn,db:Session=Depends(get_db),u=Depends(roles(UserRole.SELLER,UserRole.ADMIN))):
    if db.query(Product).filter_by(sku=x.sku).first(): raise HTTPException(400,"SKU already exists")
    p=Product(**x.model_dump(),seller_id=u.id); db.add(p); db.commit(); db.refresh(p); return p
@router.get("")
def all_products(skip:int=0,limit:int=20,db:Session=Depends(get_db)): return db.query(Product).offset(skip).limit(limit).all()
@router.get("/{pid}")
def one(pid:int,db:Session=Depends(get_db)):
    p=db.get(Product,pid)
    if not p: raise HTTPException(404,"Product not found")
    return p
@router.put("/{pid}")
def update(pid:int,x:ProductIn,db:Session=Depends(get_db),u=Depends(roles(UserRole.SELLER,UserRole.ADMIN))):
    p=db.get(Product,pid)
    if not p: raise HTTPException(404,"Product not found")
    if u.role!=UserRole.ADMIN and p.seller_id!=u.id: raise HTTPException(403,"Not your product")
    for k,v in x.model_dump().items(): setattr(p,k,v)
    db.commit(); db.refresh(p); return p
