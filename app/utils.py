import bcrypt
from datetime import datetime, timezone
from dotenv import load_dotenv
import os
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
    <div class="card h-100 shadow-sm" style="background: linear-gradient(135deg, #ff4d4d, #990000); color: white; border: none;">
       <img id="product_image"
     src="{prod[3]}" 
     class="card-img-top"
     alt="..."
     data-bs-toggle="modal" 
     data-bs-target="#imageModal"
     style="border-radius: 10px; object-fit: cover;">
        <div class="card-body">
            <div class="clearfix mb-3"> 
               <span class="float-start badge rounded-pill bg-light text-dark" id="product_name" 
                     style="font-size: 1rem; padding: 7px 10px;">{prod[0]}</span> 

                <span class="float-end price-hp fw-bold text-warning" id="product_price">{prod[2][cname]}₹</span> 
            </div>
            <h5 class="card-title" id="product_description" style="font-weight: 400; color: white;">{prod[1]}</h5>

            <div class="text-center my-4"> 
                <a href="#" class="btn" id="buynow" 
                   style="background: #ffcc00; color: #990000; font-weight: bold; border-radius: 8px;">
                   Buy Now
                </a> 
            </div>
            <div class="text-center my-4"> 
                <a href="#" class="float-end text-white fw-bold" style="text-decoration: none; color: white;" id="addcart">
                   Add To Cart
                </a> 
            </div>
        </div>
    </div>
</div>

<!-- Bootstrap Modal -->
<div class="modal fade" id="imageModal" tabindex="-1" aria-labelledby="imageModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content" style="background: #990000; color: white;">
            <div class="modal-header">
                <h5 class="modal-title" id="imageModalLabel">{prod[0]}</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body text-center">
                <img id="modalImage" src="{prod[3]}" class="img-fluid" alt="Product Image" style="border-radius: 10px;">
            </div>
        </div>
    </div>
</div>


           """
    return htmlcode



async def send_email(subject,body,to_email):
    from_email ="praveen.gopi717@gmail.com"
    from_password="nbrw kyzi zpto sezm"

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

    