import mysql.connector
from mysql.connector import pooling
import aiomysql
from fastapi import Depends


#Database pool (async)
async def get_db_pool():
    pool = await aiomysql.create_pool(
        host='127.0.0.1',  # IP address without 'http://'
        user='nibhasitsolutions',
        password='248646',
        db='hhhperfumes',  # Ensure you specify the database name here
        minsize=1,
        maxsize=5,
    )
    return pool

#insert new perfume category into perfumes_categories table---------
async def insert_category(category:str,pool:aiomysql.pool=Depends(get_db_pool)):

    try:
        async with pool.acquire() as connection:
            async with connection.cursor() as cursor:
                query="insert into perfumes_categories(categories) values(%s)"
                await cursor.execute(query,(category))
                await connection.commit()
                return {"message": "Perfume HTML code inserted successfully", "affected_rows": cursor.rowcount}
    except aiomysql.MySQLError as e:
            await connection.rollback()
            raise Exception(f'database error:{e}')
    return {"message":"insertion error"}

    

#retrieve category id from perfumes_categories table----------------
async def retrieve_category_id(category:str,pool:aiomysql.pool=Depends(get_db_pool)):
    pass
