from fastapi import FastAPI,HTTPException
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
from models import init_db,close_db,insert_category,return_all_category

import aiomysql

app=FastAPI()


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



#return json response-------------------------
@app.get("/")
def home():
    return {"hello":"world"}

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
    content= """
            <div class="col-md-4">
                <div class="card p-3 card-item">
                    <div class="d-flex flex-row mb-3"><br>
                        <img src="/static/images/first.png" width="70"><br>
                        <div class="d-flex flex-column ml-2"><span>Stripe</span><span class="text-black-50">Payment Services</span><span class="ratings"><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i></span></div>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card p-3 card-item">
                    <div class="d-flex flex-row mb-3"><img src="/static/images/second.png" width="70">
                        <div class="d-flex flex-column ml-2"><span>Mailchimp</span><span class="text-black-50">Project Management</span><span class="ratings"><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i></span></div>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card p-3 card-item">
                    <div class="d-flex flex-row mb-3"><img src="/static/images/third.png" width="70">
                        <div class="d-flex flex-column ml-2"><span>Dropbox</span><span class="text-black-50">File Management</span><span class="ratings"><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i></span></div>
                    </div>
                </div>
            </div>

    """
    content=content + """
            <div class="col-md-4">
                <div class="card p-3 card-item">
                    <div class="d-flex flex-row mb-3"><br>
                        <img src="/static/images/first.png" width="70"><br>
                        <div class="d-flex flex-column ml-2"><span>Stripe</span><span class="text-black-50">Payment Services</span><span class="ratings"><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i></span></div>
                    </div>
                </div>
            </div>
        """
    return content


@app.get("/insert")
async def new_category():
    msg= await insert_category('car perfumes')
    print(msg)
    return msg




@app.get("/list_category")
async def list_category():
    msg= await return_all_category()
    print(msg)
    return msg


from models import return_category_id
@app.get("/category_id")
async def category_id():
    msg= await return_category_id('car perfumes')
    print(msg)
    return msg
