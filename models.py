import mysql.connector
from mysql.connector import pooling
from aiomysql import create_pool,Error,DictCursor
from fastapi import Depends



#Database pool (async)
DB_CONFIG={
        "host":'127.0.0.1',  # IP address without 'http://'
        "port":3306,
        "user":'nibhasitsolutions',
        "password":'248646',
        "db":'hhhperfumes',  # Ensure you specify the database name here
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


#insert new perfume category into perfumes_categories table-----------------------------------------
async def insert_category(categories:str):
      global pool
      try:
            async with pool.acquire() as connection:
                  async with connection.cursor() as cursor:
                        await cursor.execute(
                            "insert into perfumes_categories(categories) values(%s)",(categories)
                        )
                        await connection.commit()
                        return {"success": True, "message": "categories inserted successfully"}
      except Error as e:
            return {"success": False, "message": f"Database error: {e}"}
      except Exception as e:
            return {"success": False, "message": f"Unexpected error: {e}"}



#return all categories of perfumes------------------------------------------------------------------------
async def return_all_category():
      global pool
      try:
            async with pool.acquire() as connection:
                  async with connection.cursor(DictCursor) as cursor:
                        await cursor.execute("select categories from perfumes_categories")
                        result=await cursor.fetchall()
                        return result
      except Error as e:
            return {"success": False, "message": f"Database error: {e}"}
      except Exception as e:
            return {"success": False, "message": f"Unexpected error: {e}"}


async def return_category_id(category:str):
      global pool
      try:
            async with pool.acquire() as connection:
                  async with connection.cursor(DictCursor) as cursor:
                        await cursor.execute("select id from perfumes_categories where categories=%s",(category))
                        result=await cursor.fetchone()
                        return result
      except Error as e:
            return {"success": False, "message": f"Database error: {e}"}
      except Exception as e:
            return {"success": False, "message": f"Unexpected error: {e}"}


async def insert_perfumes_details(category_id:int,perfumes_name:str,perfumes_description:str,perfumes_price:str):
      global pool
      try:
            async with pool.acquire() as connection:
                  async with connection.cursor() as cursor:
                        await cursor.execute(
                            "insert into perfumes_details ",())
                        await connection.commit()
                        return {"success": True, "message": "categories inserted successfully"}
      except Error as e:
            return {"success": False, "message": f"Database error: {e}"}
      except Exception as e:
            return {"success": False, "message": f"Unexpected error: {e}"}


      
    

#retrieve category id from perfumes_categories table----------------
async def retrieve_category_id():
    pass
