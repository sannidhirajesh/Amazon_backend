from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.database.database import engine
from app.database.models import Base
from app.routers import auth,products,cart,orders,payments
app=FastAPI(title="Amazon-like E-commerce API",version="1.0.0")
@app.on_event("startup")
def startup():
    with engine.begin() as c:
        for n,vals in [("userrole","'CUSTOMER','SELLER','ADMIN'"),("orderstatus","'PENDING','CONFIRMED','CANCELLED'"),("paymentstatus","'PENDING','SUCCESS','FAILED','REFUNDED'")]:
            c.execute(text(f"DO $$ BEGIN CREATE TYPE {n} AS ENUM ({vals}); EXCEPTION WHEN duplicate_object THEN NULL; END $$;"))
        Base.metadata.create_all(c)
    from app.database.database import SessionLocal
    from app.database.models import User,UserRole,Category,Product
    from app.core.security import hash_password
    db=SessionLocal()
    try:
        s=db.query(User).filter_by(email="seller@example.com").first()
        if not s:
            s=User(name="Demo Seller",email="seller@example.com",password_hash=hash_password("Seller@12345"),role=UserRole.SELLER); db.add(s); db.flush()
        if not db.query(User).filter_by(email="admin@example.com").first():
            db.add(User(name="Admin",email="admin@example.com",password_hash=hash_password("Admin@12345"),role=UserRole.ADMIN))
        cat=db.query(Category).filter_by(name="Electronics").first()
        if not cat: cat=Category(name="Electronics"); db.add(cat); db.flush()
        if not db.query(Product).filter_by(sku="DEMO-001").first():
            db.add(Product(seller_id=s.id,category_id=cat.id,name="Demo Wireless Headphones",description="Sample product",price=1499,brand="DemoBrand",stock=50,sku="DEMO-001",image_url="https://example.com/demo.jpg"))
        db.commit()
    finally: db.close()
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.include_router(auth.router,prefix="/api/v1/auth",tags=["Authentication"])
app.include_router(products.router,prefix="/api/v1/products",tags=["Products"])
app.include_router(cart.router,prefix="/api/v1/cart",tags=["Cart"])
app.include_router(orders.router,prefix="/api/v1/orders",tags=["Orders"])
app.include_router(payments.router,prefix="/api/v1/payments",tags=["Payments"])
@app.get("/")
def root(): return {"message":"Amazon-like E-commerce API is running","docs":"/docs"}
