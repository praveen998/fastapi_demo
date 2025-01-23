from pydantic import BaseModel
from typing import Optional

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
    product_price:int


class product_html(BaseModel):
    id:Optional[int]=None
    category_id:Optional[int] =None
    htmlcode:Optional[str]=None


