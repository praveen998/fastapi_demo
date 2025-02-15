from pydantic import BaseModel,EmailStr,constr
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import os

class Employee(BaseModel):
    name:str
    email:str
    age:Optional[int] =None


class Product_category(BaseModel):
    id:Optional[int] =None
    category:Optional[str] =None


class Product_details(BaseModel):
    category_name:str
    product_name:str
    product_description:Optional[str] =None
    product_price:Dict[str,Any]


class Delete_product(BaseModel):
    product_name:str


class product_html(BaseModel):
    id:Optional[int]=None
    category_id:Optional[int] =None
    htmlcode:Optional[str]=None


class Admin(BaseModel):
    username:str
    password:str

    # @classmethod
    # def check_auth(username:str,password:str):
    #     if username == os.getenv("admin_username") and password == os.getenv("admin_password"):
    #         return {'status':'success'}
    #     else:
    #         return {'status':'error'}

class Create_Order(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    country: str
    state:str
    address:str
    zipcode:str
    additional_info: Optional[str]=None
    total_amount:int

