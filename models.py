import mysql.connector
from mysql.connector import pooling
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
        "minsize":Query OK, 1 row affected (1.33 sec)

mysql> select * from perfumes_details;
+----+-------------+---------------+----------------------+----------------+
| id | category_id | perfumes_name | perfumes_description | perfumes_price |
+----+-------------+---------------+----------------------+----------------+
|  2 |           4 | bestone       | good perfume         |             50 |
+----+-------------+---------------+----------------------+----------------+
1 row in set (0.00 sec)

mysql> delete from perfumes_details where id=2;
1,
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


#insert new perfume category into perfumes_categories table----------------------------------------------
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



#retrun perfume category id--------------------------------------------------------------------------------------------------------------
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



#insert perfume details-----------------------------------------------------------------------------------------------------------------------
async def insert_perfumes_details(perfume_detais):
      global pool
      result=await return_category_id(perfume_detais.category_name)
      if result:
            try:
                  async with pool.acquire() as connection:
                        async with connection.cursor() as cursor:
                                await cursor.execute(
                                    "insert into perfumes_details(category_id,perfumes_name,perfumes_description,perfumes_price) values(%s,%s,%s,%s)",
                                    (result['id'],perfume_detais.perfumes_name,perfume_detais.perfumes_description,perfume_detais.perfumes_price))
                                await connection.commit()
                                return {"success": True, "message": "categories inserted successfully"}
            except Error as e:
                    return {"success": False, "message": f"Database error: {e}"}
            except Exception as e:
                    return {"success": False, "message": f"Unexpected error: {e}"}
      else:
            return {"success": False, "message": "no category found"}
              
      
    

#retrieve category id from perfumes_categories table------------------------------------------------------------------------------------
async def list_perfume_by_category(category:str):
      global pool
      result=await return_category_id(category)
      if result:
            try:
                  async with pool.acquire() as connection:
                        async with connection.cursor(DictCursor) as cursor:
                              await cursor.execute("select perfumes_name,perfumes_description,perfumes_price from perfumes_details where category_id=%s",(result['id']))
                              data=await cursor.fetchall()
                              return data
            except Error as e:
                  return {"success": False, "message": f"Database error: {e}"}
            except Exception as e:
                  return {"success": False, "message": f"Unexpected error: {e}"}
      else:
            return {"success": False, "message": "no category found"}
              
      
#d= list_perfume_by_category('car perfumes')
