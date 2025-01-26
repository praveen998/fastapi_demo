from fastapi import FastAPI,HTTPException,Request
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
from app.models import init_db,close_db,insert_category,return_all_category,list_product_by_category
from app.models import return_category_id,insert_product_details
from app.pydanticmodels import Product_category,Product_category,Employee,Product_details
from app.utils import create_new_html
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
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




#return plaintext response--------------------
@app.get("/plaintext",response_class=PlainTextResponse)
def plaintext():
    return "Hello world"


#return html response-------------------------
@app.get("/htmltext",response_class=HTMLResponse)
def htmltext():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FastAPI HTML Response</title>
    </head>
    <body>
        <h1>Hello, World!</h1>
        <p>This is an example of returning HTML from FastAPI.</p>
    </body>
    </html>
    """
    return html_content

@app.get("/media")
def getmedia():
    file_path="media/kali-linux-3840x2160-18058.jpg"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error":"file not found"}


@app.get("/products",response_class=HTMLResponse)
def getproducts():
    product_name='bestone'
    Product_details='use in car fffffffffffffff hhhhhhhhhhhhhhhhhh eeeeeeeeeeeeeeeeee'
    product_price=50

    content= """
    """
    content=content + f"""
            <div class="col-md-4">
                <div class="card p-3 card-item">
                    <div class="d-flex flex-row mb-3"><br>
                        <img src="/static/images/first.png" width="70"><br>
                        <div class="d-flex flex-column ml-2"><span>{product_name}</span><span class="text-black-50">perfume details:{Product_details}</span><span>price:{product_price}</span><span class="ratings"><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i></span></div>
                    </div>
                </div>
            </div>
        """
    return content



@app.post("/insert_category/")
async def new_category(cate:Product_category):
    msg= await insert_category(cate.category)
    print(msg)
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
    htmlcode=await create_new_html(msg)
    return htmlcode


