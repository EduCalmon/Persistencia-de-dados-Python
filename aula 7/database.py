from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'postgresql://postgres:postgres@localhost:5432/db_escola'

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine) # Fábrica de sessões

Base = declarative_base() # Serve para ter uma base de como vai ser os modelos