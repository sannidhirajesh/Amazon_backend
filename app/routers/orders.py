from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database.models import Cart,Order,OrderItem,OrderStatus,Product
from app.schemas.schemas import OrderIn
from app.core.dependencies import current_user
router=APIRouter()
@router.post("")
def place(x:OrderIn,db:Session=Depends(get_db),u=Depends(current_user)):
    c=db.query(Cart).filter_by(user_id=u.id).first()
    if not c or not c.items: raise HTTPException(400,"Cart is empty")
    try:
        o=Order(user_id=u.id,status=OrderStatus.CONFIRMED,total=0,shipping_address=x.shipping_address); db.add(o); db.flush()
        total=0
        for i in list(c.items):
            p=db.get(Product,i.product_id)
            if not p or p.stock<i.quantity: raise HTTPException(400,"Insufficient stock")
            p.stock-=i.quantity; total+=float(p.price)*i.quantity
            db.add(OrderItem(order_id=o.id,product_id=p.id,quantity=i.quantity,unit_price=p.price)); db.delete(i)
        o.total=round(total*1.18,2); db.commit(); db.refresh(o)
        return {"id":o.id,"status":o.status,"total":float(o.total)}
    except: db.rollback(); raise
@router.get("")
def mine(db:Session=Depends(get_db),u=Depends(current_user)): return db.query(Order).filter_by(user_id=u.id).order_by(Order.created_at.desc()).all()
@router.get("/{oid}")
def one(oid:int,db:Session=Depends(get_db),u=Depends(current_user)):
    o=db.get(Order,oid)
    if not o or o.user_id!=u.id: raise HTTPException(404,"Order not found")
    return o
