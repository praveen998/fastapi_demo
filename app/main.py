from fastapi import FastAPI,HTTPException,Request,Form, File, UploadFile,BackgroundTasks,Header
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
from app.models import init_db,close_db,insert_category,return_all_category,list_product_by_category,delete_category,insert_product_details,list_product_by_search_name
from app.models import return_category_id,insert_product_details,pool,delete_product_by_name,return_product_img_url
from app.pydanticmodels import Product_category,Product_category,Employee,Product_details,Admin,Delete_product,Create_Order,VerifyPaymentRequest
from app.utils import create_new_html,verify_password,verify_admin_jwt_token,create_jwt_token,convert_products_to_dict,send_email
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.database import init_ormdb
from pydantic import BaseModel
from typing import Optional, Dict, List
import json
import httpx
import razorpay
import hmac
import hashlib
from fastapi_csrf_protect import CsrfProtect
import secrets
from fastapi import Response



app=FastAPI()


# Set up the templates directory
templates = Jinja2Templates(directory="templates")
# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")




app.add_middleware(
    CORSMiddleware,
   # allow_origins=["http://ec2-3-110-174-115.ap-south-1.compute.amazonaws.com","http://souparnikahaircare.com"],  # Replace "*" with specific domains if needed
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


razorpay_client = razorpay.Client(auth=("rzp_test_2SSqGlsTH8Gc2X","3wpzNPoPk10dpsPAqiFHqlN2"))

@app.on_event("startup")
async def startup_event():
    await init_db()


@app.on_event("shutdown")
async def shutdown_event():
    await close_db()


country_name=""



@app.get("/", response_class=HTMLResponse)
async def home(request: Request, background_tasks: BackgroundTasks):
   # background_tasks.add_task(send_email,"Test Subject", "This is a test email body.", "praveengopi998@gmail.com")
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/buynow",response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("buynow.html", {"request": request})

@app.get("/cart",response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("cart.html", {"request": request})


@app.get("/admin",response_class=HTMLResponse)
async def adminpage(request: Request):
    return templates.TemplateResponse("adminlogin.html", {"request": request})



#addmin authentication--------------------------------------------------------
@app.post("/adminauth")
async def adminpage(admin:Admin):
    val=verify_password(admin.password,os.getenv('adminhash'))
    #status=Admin.check_auth(Admin.username,Admin.password)
    if val:
          token = create_jwt_token({"username": admin.username})
          return {"message": "Login successful", "status": "success","token": token}
    else:
          raise HTTPException(status_code=401, detail="Invalid username or password")
#--- ---------------------------------------------------------------------------


@app.get("/dashboard",response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/protected")
async def protected_route(user: dict = Depends(verify_admin_jwt_token)):
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
            Key=f"hhhperfumes/{file_name}",
            Body=file_content,
            ContentType=mime_type,
        )

        file_url = f"https://{S3_BUCKET_NAME}.s3.{s3_client.meta.region_name}.amazonaws.com/hhhperfumes/{file_name}"

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
    msg= await list_product_by_category(Category.category)
    global country_name
    if isinstance(msg,dict):
        return """ <h3>no item found.........</h3> """
    htmlcode=await create_new_html(msg,country_name)
    return htmlcode


@app.post("/seach_product/",response_class=HTMLResponse)
async def seach_product(Category:Product_category):
    msg=await list_product_by_search_name(Category.category)
    global country_name
    if isinstance(msg,dict):
        return """ <h3>no item found.........</h3> """
    htmlcode=await create_new_html(msg,country_name)
    return htmlcode


@app.post("/list_products_edit_product/")
async def list_product_edit_product(Category:Product_category,user: dict = Depends(verify_admin_jwt_token)):
    msg= await list_product_by_category(Category.category)
    product_dict= convert_products_to_dict(msg)
    if isinstance(msg,dict):
        raise HTTPException(status_code=401, detail="empty proudcts..")
    else:
       # htmlcode=await create_new_html(msg)
        return product_dict


async def uploadimage_to_aws(s3client,S3_BUCKET_NAME,product_img):
        file_content = await product_img.read()
        file_key = f"hhhperfumes/{product_img.filename}"

        s3client.put_object(
                Bucket=S3_BUCKET_NAME,
                Key=file_key,
                Body=file_content,
                ContentType=product_img.content_type,
            )
        file_url = f"https://{S3_BUCKET_NAME}.s3.{s3_client.meta.region_name}.amazonaws.com/{file_key}"
        return file_url


async def delete_img_from_aws(s3client,S3_BUCKET_NAME,filename):
    try:
        file_name = file_name.split("/")[-1]
        file_name=f"hhhperfumes/{file_name}"
        s3client.delete_object(Bucket=S3_BUCKET_NAME, Key=filename)
        return True
    except Exception as e:
        return False



@app.post("/add_new_product/")
async def add_product(
    product_name: str = Form(...),
    product_description: Optional[str] = Form(None),
    india_price: float = Form(...),
    uae_price: float = Form(...),
    category: str = Form(...),
    product_img: UploadFile = File(...)
): 
    print("product file name:",product_img)
    filename=await uploadimage_to_aws(s3_client,S3_BUCKET_NAME,product_img)
    print("aws file url:",filename)
    product={
        "product_name": product_name,
        "product_description": product_description,
        "product_price": {
            "India": india_price,
            "UAE": uae_price
        },
        "category": category,
        "product_image_url": filename
    }
    
    msg=await insert_product_details(product)
    print(type(product['product_name']))
    print(type(product['category']))
    print(type(product['product_image_url']))
    print(type(json.dumps(product['product_price'])))
    print(type(product['product_description']))
    return msg



@app.post("/delete_product/")
async def delete_product(req:Delete_product,user: dict = Depends(verify_admin_jwt_token)):
    if req:
        msg=await delete_product_by_name(req.product_name,s3_client,S3_BUCKET_NAME)
        return msg
    else:
        raise HTTPException(status_code=401, detail="no product name given")



@app.get("/geolocation-by-ip")
async def read_geolocation(request: Request):
    ip = request.client.host  # Get the client's IP address
    api_url = f"http://ip-api.com/json/{ip}?fields=country,lat,lon,regionName,city"
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url)
        data = response.json()
        print(data['country'])
    return data

    
@app.post("/create-order/")
async def create_order(c_order:Create_Order,request: Request):
    # token_from_cookie = request.cookies.get("csrf_token")
    # token_from_header = request.headers.get("X-CSRF-Token") 
    # print('csrf_token_cookie:',token_from_cookie)
    # print('csrf_token_header:',token_from_header)
    
    
    # if not token_from_cookie:
    #     raise HTTPException(status_code=403, detail="Missing CSRF token in cookies")

    # # (Optional) If using a double-submit method, ensure it matches
    # if token_from_header and token_from_cookie != token_from_header:
    #     raise HTTPException(status_code=403, detail="CSRF token mismatch")
    
    order_data=[]
    order_data.append(c_order.order_data)
    try:

        order_payload = {
            "amount": int(c_order.total_amount * 100),  # Convert INR to paisa
            "currency": "INR",
            "payment_capture": 1,  # Auto-capture payment
        }
        # Create order
        order_out = razorpay_client.order.create(order_payload)
        order={'id':order_out['id'],'currency':order_out['currency'],'amount':order_out['amount'],"message": "Your Order is Ready Checkout Now..!",'first_name':c_order.first_name,'last_name':c_order.last_name,'email':c_order.email,'phone':c_order.phone,'country':c_order.country,
        'state':c_order.state,'city':c_order.city,'address':c_order.address,'zipcode':c_order.zipcode,'total_amount':c_order.total_amount,'cart_data':order_data}
        return order

    except razorpay.errors.BadRequestError as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")
    except razorpay.errors.UnauthorizedError as e:
        raise HTTPException(status_code=401, detail=f"Unauthorized: {str(e)}")
    except razorpay.errors.ForbiddenError as e:
        raise HTTPException(status_code=403, detail=f"Forbidden: {str(e)}")
    except razorpay.errors.NotFoundError as e:
        raise HTTPException(status_code=404, detail=f"Not Found: {str(e)}")
    except razorpay.errors.ServerError as e:
        raise HTTPException(status_code=500, detail=f"Razorpay Server Error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")




@app.post("/verify-payment/")
async def verify_payment(data: VerifyPaymentRequest):
    try:
        # Concatenate order_id and payment_id as per Razorpay docs
        generated_signature = hmac.new("3wpzNPoPk10dpsPAqiFHqlN2".encode(),
            f"{data.razorpay_order_id}|{data.razorpay_payment_id}".encode(),
            hashlib.sha256
        ).hexdigest()

        # Compare with Razorpay's signature
        if generated_signature == data.razorpay_signature:
            return {"status": "success", "message": "Payment verified successfully!"}
        else:
            raise HTTPException(status_code=400, detail="Invalid payment signature")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@app.post("/create-order-cart/")
async def create_order_cart(request: Request):
    # token_from_cookie = request.cookies.get("csrf_token")
    # token_from_header = request.headers.get("X-CSRF-Token") 
    # print('csrf_token_cookie:',token_from_cookie)
    # print('csrf_token_header:',token_from_header)
    
    
    # if not token_from_cookie:
    #     raise HTTPException(status_code=403, detail="Missing CSRF token in cookies")

    # # (Optional) If using a double-submit method, ensure it matches
    # if token_from_header and token_from_cookie != token_from_header:
    #     raise HTTPException(status_code=403, detail="CSRF token mismatch")
      

    request_data = await request.json()
    order_data = request_data.get("order", {})
    cart_data = request_data.get("cart", [])
    total_amount=0
    for i in range(len(cart_data)):
        total_amount+=cart_data[i]['product_total']
    try:
        # Convert amount to paisa (Razorpay requires amount in paisa)
        order_payload = {
            "amount": int(total_amount * 100),  # Convert INR to paisa
            "currency": "INR",
            "payment_capture": 1,  # Auto-capture payment
        }

    except razorpay.errors.BadRequestError as e:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(e)}")
    except razorpay.errors.UnauthorizedError as e:
        raise HTTPException(status_code=401, detail=f"Unauthorized: {str(e)}")
    except razorpay.errors.ForbiddenError as e:
        raise HTTPException(status_code=403, detail=f"Forbidden: {str(e)}")
    except razorpay.errors.NotFoundError as e:
        raise HTTPException(status_code=404, detail=f"Not Found: {str(e)}")
    except razorpay.errors.ServerError as e:
        raise HTTPException(status_code=500, detail=f"Razorpay Server Error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
     
    order_out = razorpay_client.order.create(order_payload)
    order={'id':order_out['id'],'currency':order_out['currency'],'amount':order_out['amount'],"message": "Your Order is Ready Checkout Now..!",'first_name':order_data['first_name'],'last_name':order_data['last_name'],'email':order_data['email'],'phone':order_data['phone'],'country':order_data['country'],
    'state':order_data['state'],'city':order_data['city'],'address':order_data['address'],'zipcode':order_data['zipcode'],'total_amount':total_amount,'cart_data':cart_data}
    return order
    #return {"status": "success", "message": "Payment verified successfully!"}



@app.get("/csrf-token")
async def get_csrf_token(response: Response):
    csrf_token = secrets.token_hex(32)  # Generate a random CSRF token
    response.set_cookie(
        key="csrf_token",
        value=csrf_token,
        httponly=False,  # Prevent JavaScript access
        secure=True,    # Require HTTPS
        samesite="Strict"  # Prevent cross-site requests
    )
    return {"message": "CSRF token set in cookies"}




@app.post("/send_purchase_data/")
async def create_order_cart(request: Request,background_tasks: BackgroundTasks):
    request_data = await request.json()
    #print("type of request_data:",type(request_data))
    #print("customer purchase data:",request_data)
   #background_tasks.add_task(send_email,"customer data", str(request_data), "praveengopi998@gmail.com")
    return {"status": "success", "message": "Payment verified successfully!"}








