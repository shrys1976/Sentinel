from sqlalchemy.orm import DeclarativeBase, declarative_base
from sqlalchemy import Column, ColumnElement,String,Integer,DateTime
from sqlalchemy.sql import func
import uuid

class Base(DeclarativeBase):
    pass

class Dataset(Base):

    __tablename__ = "datasets"

    id = Column(

        String,
        primary_key=True,
        default = lambda: str(uuid.uuid4())
    )


    user_id = Column(String,nullable=True)
    session_id = Column(String,nullable=True)
    name = Column(String,nullable=False)
    file_path = Column(String,nullable=False)
    status = Column(String,default = "uploaded")
    rows = Column(Integer,nullable=True)
    columns =Column(Integer,nullable=True)
    
    created_at = Column(
        DateTime(timezone=True),
        server_default= func.now()
    )