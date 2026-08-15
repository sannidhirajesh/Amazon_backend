from pydantic import BaseModel,EmailStr,Field
class Register(BaseModel):
    name:str; email:EmailStr; password:str=Field(min_length=8); phone:str|None=None
class UserOut(BaseModel):
    id:int; name:str; email:EmailStr; phone:str|None; role:str
    model_config={"from_attributes":True}
class Login(BaseModel): email:EmailStr; password:str
class ProductIn(BaseModel):
    name:str; description:str|None=None; price:float=Field(gt=0); category_id:int|None=None
    brand:str|None=None; stock:int=Field(ge=0); sku:str; image_url:str|None=None
class CartIn(BaseModel): product_id:int; quantity:int=Field(gt=0)
class OrderIn(BaseModel): shipping_address:str|None=None
class PaymentIn(BaseModel): order_id:int; payment_method:str="MOCK"
