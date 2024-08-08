import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

engine = create_engine(os.getenv('DATABASE_URL'))
SessionLocal = sessionmaker()
Base = declarative_base()
