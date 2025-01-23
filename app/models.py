from aiomysql import create_pool,Error,DictCursor
from fastapi import Depends
import os 
from dotenv import load_dotenv


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



#return all categories of product------------------------------------------------------------------------
async def return_all_category():
      global pool
      try:
            async with pool.acquire() as connection:
                  async with connection.cursor(DictCursor) as cursor:
                        await cursor.execute("select categories from product_categories")
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
      result=await return_category_id(product_detais.category_name)
      if result:
            try:
                  async with pool.acquire() as connection:
                        async with connection.cursor() as cursor:
                                await cursor.execute(
                                    "insert into product_details(category_id,product_name,product_description,product_price) values(%s,%s,%s,%s)",
                                    (result['id'],product_detais.product_name,product_detais.product_description,product_detais.product_price))
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
                              await cursor.execute("select product_name,product_description,product_price from product_details where category_id = %s ",(result['id']))
                              data=await cursor.fetchall()
                              return data
            except Error as e:
                  return {"success": False, "message": f"Database error: {e}"}
            except Exception as e:
                  return {"success": False, "message": f"Unexpected error: {e}"}
      else:
            return {"success": False, "message": "no category found"}
            


      
#d= list_perfume_by_category('car perfumes')
