# from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text, JSON
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, relationship
# from datetime import datetime

# DATABASE_URL = "postgresql://user:password@localhost/dbname"
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()


# class User(Base):
#     __tablename__ = "users"
#     user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     username = Column(String, unique=True, index=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     last_login = Column(DateTime, nullable=True)

# class Dataset(Base):
#     __tablename__ = "datasets"
#     dataset_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     user_id = Column(Integer, ForeignKey('users.user_id'))
#     name = Column(String, index=True)
#     description = Column(Text, nullable=True)
#     upload_date = Column(DateTime, default=datetime.utcnow)
#     last_modified = Column(DateTime, default=datetime.utcnow)
#     file_path = Column(String)
#     user = relationship("User")

# class Task(Base):
#     __tablename__ = "tasks"
#     task_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     dataset_id = Column(Integer, ForeignKey('datasets.dataset_id'))
#     operation_type = Column(String)
#     parameters = Column(JSON)
#     status = Column(String)
#     result_path = Column(String, nullable=True)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow)
#     dataset = relationship("Dataset")

# # def create_tables():
# #     Base.metadata.create_all(bind=engine)


# models.py
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "postgresql://zhfycjmb:bdM-ujWF82U3oNrdwR2OyC1mKqj1oCjc@flora.db.elephantsql.com/zhfycjmb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Dataset(Base):
    __tablename__ = "datasets"
    dataset_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    upload_date = Column(DateTime, default=datetime.utcnow)
    last_modified = Column(DateTime, default=datetime.utcnow)
    file_path = Column(String)

Base.metadata.create_all(engine)
# pip install python-multipart
# uvicorn main:app --reload
# source env/Scripts/activate
# python -m venv env