from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database.models import Cart,CartItem,Product
from app.schemas.schemas import CartIn
from app.core.dependencies import current_user
router=APIRouter()
def cart(db,u):
    c=db.query(Cart).filter_by(user_id=u.id).first()
    if not c: c=Cart(user_id=u.id); db.add(c); db.commit(); db.refresh(c)
    return c
@router.post("/items")
def add(x:CartIn,db:Session=Depends(get_db),u=Depends(current_user)):
    p=db.get(Product,x.product_id)
    if not p: raise HTTPException(404,"Product not found")
    if p.stock<x.quantity: raise HTTPException(400,"Insufficient stock")
    c=cart(db,u); i=db.query(CartItem).filter_by(cart_id=c.id,product_id=p.id).first()
    if i: i.quantity+=x.quantity
    else: db.add(CartItem(cart_id=c.id,product_id=p.id,quantity=x.quantity))
    db.commit(); return {"message":"Item added"}
@router.get("")
def get(db:Session=Depends(get_db),u=Depends(current_user)):
    c=cart(db,u); items=[]; subtotal=0
    for i in c.items:
        t=float(i.product.price)*i.quantity; subtotal+=t
        items.append({"id":i.id,"product_id":i.product_id,"quantity":i.quantity,"unit_price":float(i.product.price),"item_total":t})
    tax=round(subtotal*.18,2)
    return {"items":items,"subtotal":subtotal,"discount":0,"tax":tax,"final_total":subtotal+tax}
