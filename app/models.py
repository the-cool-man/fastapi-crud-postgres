from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Post(Base):
    __tablename__ = "posts"

    # For Postgres
    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, nullable=True, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


    # For MySQL
    # id = Column(Integer, primary_key = True, nullable = False, index=True)
    # title = Column(String(255), nullable = False)
    # content = Column(String(255), nullable = False)
    # published = Column(Boolean,default=TRUE)
    # created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, nullable = False)
    email = Column(String, nullable = False)
    password = Column(String, nullable = False)
    userType = Column(String, nullable = False, server_default=text('D'))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    
