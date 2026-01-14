
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "postgresql://postgres:Password@localhost/Products"
engine = create_engine(db_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)