from fastapi import FastAPI,HTTPException,Request,Form, File, UploadFile
from fastapi.responses import PlainTextResponse
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
import os
from fastapi import File,UploadFile,HTTPException
from botocore.exceptions import BotoCoreError,ClientError
import boto3
from dotenv import load_dotenv
import mimetypes
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends
from app.models import init_db,close_db,insert_category,return_all_category,list_product_by_category,delete_category,insert_product_details
from app.models import return_category_id,insert_product_details,pool
from app.pydanticmodels import Product_category,Product_category,Employee,Product_details,Admin
from app.utils import create_new_html,verify_password,verify_admin_jwt_token,create_jwt_token,convert_products_to_dict
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.database import init_ormdb
from pydantic import BaseModel
from typing import Optional, Dict, List
import json
import httpx


app=FastAPI()


# Set up the templates directory
templates = Jinja2Templates(directory="templates")
# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")




app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific domains if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


init_ormdb()
load_dotenv()
# AWS S3 Configuration

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")



# Initalize S3 Client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)


@app.on_event("startup")
async def startup_event():
    await init_db()


@app.on_event("shutdown")
async def shutdown_event():
    await close_db()




@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/buynow", response_class=HTMLResponse)
async def buynow(request: Request):
    return templates.TemplateResponse("buynow.html", {"request": request})


@app.get("/cart", response_class=HTMLResponse)
async def cart(request: Request):
    return templates.TemplateResponse("cart.html", {"request": request})


@app.post("/employee/")
async def create_eployee(emp:Employee):
    print('type of age:',type(emp.age))
    print('type of name:',type(emp.name))
    return {'message':f'employee{emp.name} has been created','data':emp}


@app.get("/admin",response_class=HTMLResponse)
async def adminpage(request: Request):
    return templates.TemplateResponse("adminlogin.html", {"request": request})




#addmin authentication--------------------------------------------------------
@app.post("/adminauth")
async def adminpage(admin:Admin):
    print('username:',admin.username)
    print('password:',admin.password)
    val=verify_password(admin.password,os.getenv('adminhash'))
    #status=Admin.check_auth(Admin.username,Admin.password)
    if val:
          token = create_jwt_token({"username": admin.username})
          print(token)
          return {"message": "Login successful", "status": "success","token": token}
    else:
          raise HTTPException(status_code=401, detail="Invalid username or password")
#--- ---------------------------------------------------------------------------


@app.get("/dashboard",response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/protected")
async def protected_route(user: dict = Depends(verify_admin_jwt_token)):
    print(user)
    return {"message": "Access granted", "user": user}




@app.get("/upload")
def upload():
    try:
        file_path = 'media/kali-linux-3840x2160-18058.jpg'  # Replace with your file path
        # Read the file content
        file_name = os.path.basename(file_path)  # Extracts the filename from the full path (e.g., "kali-linux-3840x2160-18058.jpg")

        mime_type, _ = mimetypes.guess_type(file_path)

        with open(file_path, 'rb') as file:
            file_content = file.read()
        # Upload to S3
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=file_name,
            Body=file_content,
            ContentType=mime_type,
        )
        file_url = f"https://{S3_BUCKET_NAME}.s3.{s3_client.meta.region_name}.amazonaws.com/{file_name}"

        return {"message": f"File '{file_url}' uploaded successfully to S3 bucket '{S3_BUCKET_NAME}'."}
    
    except (BotoCoreError, ClientError) as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")




@app.get("/media")
def getmedia():
    file_path="media/kali-linux-3840x2160-18058.jpg"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error":"file not found"}



@app.post("/insert_category/")
async def new_category(cate:Product_category,user: dict = Depends(verify_admin_jwt_token)):
    msg= await insert_category(cate.category)
    print(msg)
    print(user)
    return msg


@app.post("/delete_category/")
async def delete_product_category(cate:Product_category,user: dict = Depends(verify_admin_jwt_token)):
    msg= await delete_category(cate.id)
    print(msg)
    print(user)
    return msg



@app.get("/list_category")
async def list_category():
    msg= await return_all_category()
    return msg



@app.get("/category_id")
async def category_id():
    msg= await return_category_id('car perfume')
    print(msg)
    return msg



@app.post("/insert_product_details/")
async def category_id(product:Product_details):
    msg= await insert_product_details(product)
    print(msg)
    return msg


#return products based on product category


@app.post("/list_products/",response_class=HTMLResponse)
async def list_product(Category:Product_category):
    print('category:',Category.category)
    msg= await list_product_by_category(Category.category)
    if isinstance(msg,dict):
        return """ <h3>no item found.........</h3> """
    htmlcode=await create_new_html(msg)
    return htmlcode



@app.post("/list_products_edit_product/")
async def list_product_edit_product(Category:Product_category,user: dict = Depends(verify_admin_jwt_token)):
    print('category:',Category.category)
    msg= await list_product_by_category(Category.category)
    product_dict= convert_products_to_dict(msg)
    if isinstance(msg,dict):
        raise HTTPException(status_code=401, detail="empty proudcts..")
    else:
       # htmlcode=await create_new_html(msg)
        return product_dict



@app.post("/add_new_product/")
async def add_product(
    product_name: str = Form(...),
    product_description: Optional[str] = Form(None),
    india_price: float = Form(...),
    uae_price: float = Form(...),
    category: str = Form(...),
    product_img: UploadFile = File(...)
):  
    product={
        "product_name": product_name,
        "product_description": product_description,
        "product_price": {
            "India": india_price,
            "UAE": uae_price
        },
        "category": category,
        "product_image_url": product_img.filename
    }
    msg=await insert_product_details(product)
    print(type(product['product_name']))
    print(type(product['category']))
    print(type(product['product_image_url']))
    print(type(json.dumps(product['product_price'])))
    print(type(product['product_description']))
    return msg




@app.get("/geolocation-by-ip")
async def read_geolocation(request: Request):
    ip = request.client.host  # Get the client's IP address
    api_url = f"http://ip-api.com/json/{ip}?fields=country,lat,lon,regionName,city"
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url)
        data = response.json()
    return data

