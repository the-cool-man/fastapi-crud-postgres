from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PostGres
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:root@localhost/fastapi'

# MySQL
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/fastapi"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()