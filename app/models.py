from aiomysql import create_pool,Error,DictCursor
from fastapi import Depends
import os 
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, Boolean,ForeignKey,JSON
from app.database import Base
import json


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    email = Column(String(100), unique=True, index=True)
    is_active = Column(Boolean, default=True)


class Product_categories(Base):
      __tablename__ = "product_categories"
      
      id=Column(Integer,primary_key=True,index=True)
      categories=Column(String(100),unique=True,nullable=False,index=True)


class Product_details(Base):
      __tablename__ = "product_details"

      id = Column(Integer,primary_key=True,index=True)
      product_name= Column(String(100),unique=True,nullable=False,index=True)
      product_description= Column(String(500))
      product_price=Column(JSON,nullable=False)
      product_img_url=Column(String(100))
      category_id=Column(Integer,ForeignKey("product_categories.id"))


class Client_payment(Base):
      __tablename__ = "client_payment"

      id=Column(Integer,primary_key=True,index=True)
      payment_id=Column(String(100),unique=True,nullable=False,index=True)
      customer_name=Column(String(100))
      customer_phone=Column(String(15))
      customer_email=Column(String(100))
      customer_country=Column(String(100))
      customer_state=Column(String(100))
      customer_address=Column(String(200))


class Payment_details(Base):
      __tablename__ = "payment_details"

      id =Column(Integer,primary_key=True,index=True)
      product_purchase_list=Column(JSON)
      total_amount=Column(Integer)
      client_payment_id=Column(String(100),ForeignKey("client_payment.payment_id"))


load_dotenv()
#Database pool (async)
'''
DB_CONFIG={
        "host":'127.0.0.1',  # IP address without 'http://'
        "port":3306,
        "user":'nibhasitsolutions',
        "password":'248646',
        "db":'hhhperfumes',  # Ensure you specify the database name here
        "minsize":1,
        "maxsize":5,
        }
'''


DB_CONFIG={
        "host":os.getenv('host'),  # IP address without 'http://'
        "port":int(os.getenv('port')),
        "user":os.getenv('user'),
        "password":os.getenv('password'),
        "db":os.getenv('db'),  # Ensure you specify the database name here
        "minsize":1,
        "maxsize":5,
        }

pool =None

async def init_db():
      global pool
      pool=await create_pool(**DB_CONFIG)


async def close_db():
      global pool
      if pool:
            pool.close()
            await pool.wait_closed()


#insert new product category into product_categories table----------------------------------------------
async def insert_category(categories:str):
      global pool
      try:
            async with pool.acquire() as connection:
                  async with connection.cursor() as cursor:
                        await cursor.execute(
                            "insert into product_categories(categories) values(%s)",(categories)
                        )
                        await connection.commit()
                        return {"success": True, "message": "categories inserted successfully"}
      except Error as e:
            return {"success": False, "message": f"Database error: {e}"}
      except Exception as e:
            return {"success": False, "message": f"Unexpected error: {e}"}


#delete category by id-----------------------------------------------------------------------------
async def delete_category(id:int):
      global pool
      try:
            async with pool.acquire() as connection:
                  async with connection.cursor() as cursor:
                        await cursor.execute(
                            "delete from product_categories where id=%s",(id)
                        )
                        await connection.commit()
                        return {"success": True, "message": "categories deleted successfully"}
      except Error as e:
            return {"success": False, "message": f"Database error: {e}"}
      except Exception as e:
            return {"success": False, "message": f"Unexpected error: {e}"}



#return all categories of product------------------------------------------------------------------------
async def return_all_category():
      global pool
      try:
            async with pool.acquire() as connection:
                  async with connection.cursor(DictCursor) as cursor:
                        await cursor.execute("select id,categories from product_categories")
                        result=await cursor.fetchall()
                        return result
      except Error as e:
            return {"success": False, "message": f"Database error: {e}"}
      except Exception as e:
            return {"success": False, "message": f"Unexpected error: {e}"}




#retrun product category id--------------------------------------------------------------------------------------------------------------
async def return_category_id(category:str):
      global pool
      try:
            async with pool.acquire() as connection:
                  async with connection.cursor(DictCursor) as cursor:
                        await cursor.execute("select id from product_categories where categories=%s",(category))
                        result=await cursor.fetchone()
                        return result
      except Error as e:
            return {"success": False, "message": f"Database error: {e}"}
      except Exception as e:
            return {"success": False, "message": f"Unexpected error: {e}"}



#insert product details-----------------------------------------------------------------------------------------------------------------------
async def insert_product_details(product_detais):
      global pool
      result=await return_category_id(product_detais['category'])
      if result:
            try:
                  async with pool.acquire() as connection:
                        async with connection.cursor() as cursor:
                                await cursor.execute(
                                    "insert into product_details(product_name,product_description,product_price,product_img_url,category_id) values(%s,%s,%s,%s,%s)",
                                    (product_detais['product_name'],product_detais['product_description'],json.dumps(product_detais['product_price']),product_detais['product_image_url'],result['id']))
                                await connection.commit()
                                return {"success": True, "message": "categories inserted successfully"}
            except Error as e:
                    return {"success": False, "message": f"Database error: {e}"}
            except Exception as e:
                    return {"success": False, "message": f"Unexpected error: {e}"}
      else:
            return {"success": False, "message": "no category found"}



#retrieve list of product from product_details table-------------------------------------------------------------------------------------------
async def list_product_by_category(category:str):
      global pool
      result=await return_category_id(category)
      if result:
            try:
                  async with pool.acquire() as connection:
                        async with connection.cursor(DictCursor) as cursor:
                              await cursor.execute("select product_name,product_description,product_price,product_img_url from product_details where category_id = %s ",(result['id']))
                              data=await cursor.fetchall()
                              return data
            except Error as e:
                  return {"success": False, "message": f"Database error: {e}"}
            except Exception as e:
                  return {"success": False, "message": f"Unexpected error: {e}"}
      else:
            return {"success": False, "message": "no category found"}
            
async def list_product_by_search_name(name:str):
      global pool
      print(type(name))
      try:
            async with pool.acquire() as connection:
                  async with connection.cursor(DictCursor) as cursor:
                        await cursor.execute("select product_name,product_description,product_price,product_img_url from product_details where product_name like %s",(f'%{name}%'))
                        data=await cursor.fetchall()
                        return data
      except Error as e:
            return {"success": False, "message": f"Database error: {e}"}
      except Exception as e:
            return {"success": False, "message": f"Unexpected error: {e}"}
      else:
            return {"success": False, "message": "no product found"}


async def return_product_img_url(product_name:str):
      global pool
      try:
            async with pool.acquire() as connection:
                  async with connection.cursor(DictCursor) as cursor:
                        await cursor.execute("select product_img_url from product_details where product_name = %s",(product_name))
                        data=await cursor.fetchall()
                        return data
      except Error as e:
            return {"success": False, "message": f"Database error: {e}"}
      except Exception as e:
            return {"success": False, "message": f"Unexpected error: {e}"}
      else:
            return {"success": False, "message": "no product found"}
      

async def delete_img_from_aws(s3client,S3_BUCKET_NAME,filename):
    print("filename:",filename)
    try:
        filename = filename.split("/")[-1]
        filename=f"hhhperfumes/{filename}"
        print("filename:",filename)
        s3client.delete_object(Bucket=S3_BUCKET_NAME,Key=filename)
        return True
    except Exception as e:
        print(e)
        return False


async def delete_product_by_name(product_name:str,s3client,S3_BUCKET_NAME):
      global pool
      data=await return_product_img_url(product_name)
      print(type(data))
      if isinstance(data,list):
            status=await delete_img_from_aws(s3client,S3_BUCKET_NAME,data[0]['product_img_url'])
            print("status:",status)
      else:
            return {"success": False, "message": f"Unexpected error: product_img_url not found"}
      if status:
            try:
                  async with pool.acquire() as connection:
                              async with connection.cursor() as cursor:
                                    await cursor.execute("delete from product_details where product_name=%s",(product_name))
                                    await connection.commit()
                                    return {"success": True, "message": "product deleted successfully"}
            except Error as e:
                        return {"success": False, "message": f"Database error: {e}"}
            except Exception as e:
                        return {"success": False, "message": f"Unexpected error: {e}"}
      else:
            return {"success": False, "message": f"Unexpected error: can't delete product_img"}




#d= list_perfume_by_category('car perfumes')
