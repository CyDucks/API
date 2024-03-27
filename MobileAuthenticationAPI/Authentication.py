import datetime
import jwt
from passlib.context import CryptContext
from fastapi import status
import hashlib
# from models import Register
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import bcrypt

SECRET_KEY = "secret_key"
ALGORITHM = "HS256"


def hash_pass(password: str):

    password_bytes = password.encode('utf-8')
    
    # Create a new SHA-256 hash object
    sha256 = hashlib.sha256()
    
    # Update the hash object with the password bytes
    sha256.update(password_bytes)
    
    # Get the hexadecimal representation of the hashed password
    hashed_password = sha256.hexdigest()
    
    return hashed_password

def create_access_token(data: dict, expires_delta: datetime.timedelta):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



# def authenticate_user(email: str, password: str, db: Session):
#     user = db.query(Register).filter(Register.Email_id == email).first()
#     if user and verify_password(password, user.password):
#         return user
#     return None


def decode_token(auth: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    token = auth.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
