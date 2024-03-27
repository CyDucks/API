from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class User(Base):
    __tablename__ = "Users"
    ID = Column(Integer, primary_key=True, index=True)
    phone = Column(String(15))
    otp = Column(String(10))
    isActive = Column(Boolean)
    token = Column(String(40))

class Mod(Base):
    __tablename__ = "Mods"
    ID = Column(Integer, primary_key=True, index=True)
    phone = Column(String(15))
    email = Column(String(30))
    St_ID = Column(String(10))
    otp = Column(String(10))
    isActive = Column(Boolean)
    token = Column(String(40))
    password = Column(String(40))


