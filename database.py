from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError

# Create an SQLite database URL for an example, modify for other DBs
SQLALCHEMY_DATABASE_URL = 'postgresql://lendnext_db:Merc$0878@lendnext-database.cds0k8iyq3dv.ap-south-1.rds.amazonaws.com:5432/lendnextdb'
# SQLALCHEMY_DATABASE_URL = 'postgresql://lendnext_test:lendnext_test!@lendnext-test.cds0k8iyq3dv.ap-south-1.rds.amazonaws.com:5432/lendnext_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
