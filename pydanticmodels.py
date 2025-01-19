from pydantic import BaseModel
from typing import Optional

class Employee(BaseModel):
    name:str
    email:str
    age:Optional[int] =None

class Perfume_category(BaseModel):
    id:Optional[int] =None
    category:Optional[str] =None

class Perfumes_details(BaseModel):
    category_name:str
    perfumes_name:str
    perfumes_description:Optional[str] =None
    perfumes_price:int


class perfumes_html(BaseModel):
    id:Optional[int]=None
    category_id:Optional[int] =None
    htmlcode:Optional[str]=None

