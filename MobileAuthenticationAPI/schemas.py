from pydantic import BaseModel, Field


class UserOTPRequest(BaseModel):
    Phone_Number: str = Field(max_length=15)

class ModOTPRequest(BaseModel):
    Phone_Number: str = Field(max_length=15)
    email: str = Field(max_length=30)
    St_ID: str = Field(max_length=10)
    password: str = Field(max_length=40)

class ModLoginRequest(BaseModel):
    Phone_Number: str = Field(max_length=15)
    password: str = Field(max_length=40)

class OTPVerificationRequest(BaseModel):
    Phone_Number: str = Field(max_length=15)
    otp: str

class ModOTPVerificationRequest(BaseModel):
    Phone_Number: str = Field(max_length=15)
    otp: str
    St_ID: str


class LogoutRequest(BaseModel):
    Phone_Number: str = Field(max_length=15)
