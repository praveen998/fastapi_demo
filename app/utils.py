import bcrypt
from datetime import datetime, timezone
from dotenv import load_dotenv
import os
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer

import json

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Token expires in 1 hour
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="adminauth")



def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()  # Generate salt
    hashed = bcrypt.hashpw(password.encode(), salt)  # Hash password
    return hashed.decode()  # Convert bytes to string

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against a stored hash."""
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def create_jwt_token(data: dict, expires_in: int = 1):
    """ Create JWT Token with expiration """
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_in)
    data.update({"exp": expire.timestamp()})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)



def verify_admin_jwt_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Return user data if valid
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")







async def create_new_html(msg):
    htmlcode="""
    """
    for i in msg:
        prod=[]
        c=0
        for key,value in i.items():
            if c==2:
                prod.append(json.loads(value))
            else:
                prod.append(value)
                c+=1
        htmlcode+=f""" 
                <div class="col">
                            <div class="card h-100 shadow-sm"> <img id="product_image"
                                    src="https://www.freepnglogos.com/uploads/notebook-png/download-laptop-notebook-png-image-png-image-pngimg-2.png"
                                    class="card-img-top" alt="...">
                                <div class="card-body">
                                    <div class="clearfix mb-3"> <span class="float-start badge rounded-pill bg-primary" id="product_name">{prod[0]}
                                            </span> <span class="float-end price-hp" id="product_price">{prod[2]['inr']}₹</span> </div>
                                    <h5 class="card-title" id="product_description">{prod[1]}</h5>
                                   <div class="text-center my-4"> <a href="" class="btn btn-warning" id="buynow">Buy Now</a> </div>
                                   <div class="text-center my-4"> <a href="" class="float-end price-hp" style="text-decoration: none;" id="addcart" >Add To Cart</a> </div>
                               
                                </div>
                            </div>
                </div>

           """
    return htmlcode


