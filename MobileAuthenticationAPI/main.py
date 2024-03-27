import datetime

from fastapi import FastAPI, HTTPException, Depends, Body
from starlette import status
from twilio.rest import Client
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models
import schemas
import random
from models import User, Mod
from Authentication import hash_pass, create_access_token, decode_token
from database import engine, SessionLocal


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


TWILIO_ACCOUNT_SID = 'AC08c5fda409cf46c247ff717dc38052a8'
TWILIO_AUTH_TOKEN = 'e7639337055259e79a0cb9b2aa62d673'
TWILIO_PHONE_NUMBER = '+447488898102'

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

valid_st_ids = ['123', '345', '456', '567', '789', '9999']

def generate_otp() -> str:
    return str(random.randint(10000, 99999))


@app.post("/user/otp_request", tags=["OTP_send_validation"])
async def send_otp(otp_request: schemas.UserOTPRequest, db: Session = Depends(get_db)):
    mobile_number = otp_request.Phone_Number
    formatted_mobile_number = '+91' + ''.join(filter(str.isdigit, mobile_number))
    otp = generate_otp()

    # Check if the user with the provided phone number already exists
    existing_user = db.query(models.User).filter(models.User.phone == mobile_number).first()

    if existing_user:
        # If the user exists, update the OTP in the user table
        existing_user.otp = otp
        db.commit()
        message = client.messages.create(
            body=f'Your SATARK OTP is: {otp}',
            from_=TWILIO_PHONE_NUMBER,
            to=formatted_mobile_number
        )
    else:
        # If the user doesn't exist, create a new user entry with the provided phone number and OTP
        new_user = models.User(phone=mobile_number, otp=otp)
        db.add(new_user)
        db.commit()
        message = client.messages.create(
            body=f'Your SATARK OTP is: {otp}',
            from_=TWILIO_PHONE_NUMBER,
            to=formatted_mobile_number
        )
        
    response = {"message": "OTP sent successfully"}

    return response

@app.post("/mod/register_otp_request", tags=["OTP_send_validation"])
async def send_otp(otp_request: schemas.ModOTPRequest, db: Session = Depends(get_db)):
    mobile_number = otp_request.Phone_Number
    email = otp_request.email
    St_id = otp_request.St_ID
    password = otp_request.password
    password = hash_pass(password)
    formatted_mobile_number = '+91' + ''.join(filter(str.isdigit, mobile_number))
    otp = generate_otp()

    # Check if the user with the provided phone number already exists
    existing_user = db.query(models.Mod).filter(models.Mod.phone == mobile_number).first()

    if existing_user:
        # If the user exists
        raise HTTPException(status_code=401, detail="User Already Registered!!")
    else:
        # If the user doesn't exist, create a new user entry with the provided phone number and OTP
        new_user = models.Mod(phone=mobile_number, otp=otp, email=email, isActive=True, St_ID=St_id, password=password)
        db.add(new_user)
        db.commit()
        message = client.messages.create(
            body=f'Your SATARK OTP is: {otp}',
            from_=TWILIO_PHONE_NUMBER,
            to=formatted_mobile_number
        ) 
        return {"message": "OTP sent successfully"}


@app.post("/mod/login_otp_request", tags=["OTP_send_validation"])
async def send_otp(otp_request: schemas.ModLoginRequest, db: Session = Depends(get_db)):
    mobile_number = otp_request.Phone_Number
    password = otp_request.password
    password = hash_pass("admin")

    # Check if the user with the provided phone number already exists
    existing_user = db.query(models.Mod).filter(models.Mod.phone == mobile_number).first()

    if existing_user:
        print(existing_user.password)
        print(password)
        # If the user exists, update the OTP in the user table
        if existing_user.password == password:
            access_token_expires = datetime.timedelta(days=1)
            access_token = create_access_token(data={"sub": existing_user.phone}, expires_delta=access_token_expires)
            existing_user.token = access_token
            db.commit()
            return {"message": "Login Successful!!", "token": access_token, "token_type": "bearer", "phone": mobile_number}
        else:
            raise HTTPException(status_code=500, detail="Invalid password")
    else:
        raise HTTPException(status_code=401, detail="No User Found!!")

@app.post("/user/otp_validation_request",tags=["OTP_send_validation"])
async def verify_otp(otp_validation_request: schemas.OTPVerificationRequest, db: Session = Depends(get_db)):
    entered_otp = otp_validation_request.otp
    mobile_number = otp_validation_request.Phone_Number

    # Retrieve OTP information from the database
    otp_info = db.query(models.User).filter(models.User.phone == mobile_number).first()

    if entered_otp == otp_info.otp:
        otp_info.isActive = True
        access_token_expires = datetime.timedelta(days=1)
        access_token = create_access_token(data={"sub": otp_info.phone}, expires_delta=access_token_expires)
        otp_info.token = access_token
        otp_info.otp = ""
        db.commit()
        return {"message": "OTP verification successful", "token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid OTP")
    
@app.post("/mod/otp_validation_request",tags=["OTP_send_validation"])
async def verify_otp(otp_validation_request: schemas.ModOTPVerificationRequest, db: Session = Depends(get_db)):
    entered_otp = otp_validation_request.otp
    mobile_number = otp_validation_request.Phone_Number

    # Retrieve OTP information from the database
    otp_info = db.query(models.Mod).filter(models.Mod.phone == mobile_number).first()
    if otp_info.St_ID not in valid_st_ids:
        raise HTTPException(status_code=401, detail="Invalid Station ID")
    elif entered_otp == otp_info.otp:
        otp_info.isActive = True
        access_token_expires = datetime.timedelta(days=1)
        access_token = create_access_token(data={"sub": otp_info.phone}, expires_delta=access_token_expires)
        otp_info.token = access_token
        otp_info.otp = ""
        db.commit()
        return {"message": "OTP verification successful", "token": access_token, "token_type": "bearer", "phone": mobile_number}
    else:
        raise HTTPException(status_code=401, detail="Invalid OTP")





# @app.post('/Login',tags=["Login_Logout"])
# def login_for_access_token(form_data: schemas.User_login, db: Session = Depends(get_db)):
#     user = authenticate_user(form_data.Email_id, form_data.password, db)
#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid credentials", )

#     access_token_expires = datetime.timedelta(days=365000)
#     access_token = create_access_token(data={"sub": user.Email_id}, expires_delta=access_token_expires)
#     login_info = models.Login(Email_id=user.Email_id, password=user.password, Token=access_token)
#     db.add(login_info)
#     db.commit()
#     return {"token_type": "bearer", "access_token": access_token}

# @app.post('/Protection_check', tags=["Login"])
# def protected_route(decoded_token: dict = Depends(decode_token)):
#     return {"message": "This is a protected route", "decoded_token": decoded_token}


@app.post('/mod/logout', tags=["Logout"])
async def logout(logout_request: schemas.LogoutRequest, db: Session = Depends(get_db)):

    mobile_number = logout_request.Phone_Number
    login_info = db.query(models.Mod).filter(models.Mod.phone == mobile_number).first()
    if login_info:
        login_info.token = ""
        db.commit()
        return {"message": "Logout successful"}
    else:
        raise HTTPException(status_code=401, detail="Unable to LogOut!!")
