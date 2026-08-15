from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database.models import Payment,PaymentStatus,Order
from app.schemas.schemas import PaymentIn
from app.core.dependencies import current_user
router=APIRouter()
@router.post("")
def pay(x:PaymentIn,db:Session=Depends(get_db),u=Depends(current_user)):
    o=db.get(Order,x.order_id)
    if not o or o.user_id!=u.id: raise HTTPException(404,"Order not found")
    if db.query(Payment).filter_by(order_id=o.id).first(): raise HTTPException(400,"Payment already exists")
    p=Payment(order_id=o.id,method=x.payment_method,status=PaymentStatus.SUCCESS); db.add(p); db.commit(); db.refresh(p); return p
