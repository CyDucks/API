from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import quote_plus

username = "postgres"
password = "ekansh"
host = "localhost"
database = "postgres"

# URL-encode the password
encoded_password = quote_plus(password)

# Create the connection string
DATABASE_URL = f"postgresql://{username}:{encoded_password}@{host}/{database}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

