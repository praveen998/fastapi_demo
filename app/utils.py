import bcrypt
from datetime import datetime, timezone
import os
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv


load_dotenv()

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()  # Generate salt
    hashed = bcrypt.hashpw(password.encode(), salt)  # Hash password
    return hashed.decode()  # Convert bytes to string

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against a stored hash."""
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def create_jwt_token(data: dict, expires_in: int = 60):
    """ Create JWT Token with expiration """
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_in)
    data.update({"exp": expire.timestamp()})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


SECRET_KEY = os.getenv("SECRET_KEY")  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Token expires in 1 hour
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="adminauth")


def verify_admin_jwt_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Return user data if valid
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def convert_products_to_dict(msg):
    product_dict={}
    j=0
    for i in msg:
        prod=[]
        c=0
        for key,value in i.items():
            if c==2:
              prod.append(json.loads(value))
            else:
                prod.append(value)
            c+=1
        j+=1
        product_dict[j]=prod
    return product_dict
    



async def create_new_html(msg,country_name):
    print("country name:",country_name)
    if country_name == "India":
        cname = "India" 
    elif country_name == "UAE":
        cname = "UAE"
    else:
        cname="India"

    htmlcode="""
    """
    for i in msg:
       
        prod=[]
        c=0
        for key,value in i.items():
            if c==2:
              prod.append(json.loads(value))
              pass
            else:
                 prod.append(value)
            c+=1

        htmlcode+=f"""
  <div class="col">
                            <div class="card h-100 shadow-sm" style="background: #f8f9fa; border-radius: 15px; border-color: red; overflow: hidden;">
                                <!-- Full image view with aspect ratio maintained -->
                                <div class="text-center d-flex justify-content-center align-items-center" style="width: 100%; height: 300px; overflow: hidden;">
                                    <img id="product_image"
                                         src="{prod[3]}"
                                         class="card-img-top"
                                         alt="Product Image"
                                         data-bs-toggle="modal"
                                         data-bs-target="#imageModal"
                                         style="max-width: 100%; max-height: 100%; object-fit: contain;">
                                </div>
                                
                                <div class="card-body d-flex flex-column justify-content-between text-center">
                                    <div>
                                        <p class="card-title text-dark fw-bold" id="product_name" style="font-size: 16px;">{prod[0]}</p>
                                        <p class="card-text text-dark" id="product_description" style="font-size: 14px;">{prod[1]}</p>
                                        <div class="mb-3">
                                            <span class="badge rounded-pill bg-light text-dark"
                                                  style="font-size: 1rem; padding: 7px 10px;" id="product_price">{prod[2][cname]}₹</span>
                                        </div>
                                    </div>
                                    <!-- Buttons with hover effect -->
                                    <div class="d-flex justify-content-between">
                                        <a href="#" class="btn btn-danger w-50 me-2 buy-now" id="buynow"
                                           style="border-radius: 8px; transition: 0.3s; font-weight: bold;">
                                           Buy Now
                                        </a>
                                        <a href="#" class="btn btn-outline-danger w-50 add-cart" id="addcart"
                                           style="border-radius: 8px; transition: 0.3s; font-weight: bold;">
                                           Add To Cart
                                        </a>
                                    </div>
                                </div>
                            </div>

                </div>        
                    
                    """

    return htmlcode



async def send_email(subject,body,to_email):
    from_email ="hhhperfumesshop@gmail.com"
    from_password=os.getenv("smtppassword")

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body,"plain"))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        #server = smtplib.SMTP('smtp.hostinger.com', 465)
        server.starttls()  # Start TLS encryption   
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()  # Close the connection
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")

    
# print("perfume hash:",hash_password("hhhperfumes1234"))