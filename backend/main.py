# from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from sqlalchemy.orm import Session
# from jose import jwt
# from passlib.context import CryptContext
# import pandas as pd
# from models import User, Dataset, Task, engine, SessionLocal, Base
# import shutil
# import os

# # Replace this with your actual database URL
# DATABASE_URL = "postgresql://user:password@localhost/dbname"
# SECRET_KEY = "your-secret-key"
# ALGORITHM = "HS256"

# Base.metadata.create_all(bind=engine)

# app = FastAPI()
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # Dependency to get DB session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # Dependency to get the current user
# async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = username
#     except jwt.JWTError:
#         raise credentials_exception
#     user = db.query(User).filter(User.username == token_data).first()
#     if user is None:
#         raise credentials_exception
#     return user

# # POST /token for testing purposes (to generate a JWT token)
# @app.post("/token", response_model=Token)
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = authenticate_user(db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}

# # Your user registration, dataset management, and transformation endpoints go here

# # Here's an example of dataset uploading
# @app.post("/datasets/upload")
# async def upload_dataset(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     # Save the uploaded file to disk
#     file_location = f"some_directory/{file.filename}"
#     with open(file_location, "wb+") as file_object:
#         shutil.copyfileobj(file.file, file_object)
    
#     # Create dataset entry in the database
#     dataset = Dataset(user_id=current_user.user_id, name=file.filename, file_path=file_location)
#     db.add(dataset)
#     db.commit()
#     db.refresh(dataset)
#     return {"filename": file.filename, "file_path": file_location}

# # Here's an example of a transform operation
# @app.post("/datasets/{dataset_id}/transform")
# async def transform_dataset(dataset_id: int, operation: str, params: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     dataset = db.query(Dataset).filter(Dataset.user_id == current_user.user_id, Dataset.dataset_id == dataset_id).first()
#     if not dataset:
#         raise HTTPException(status_code=404, detail="Dataset not found")
    
#     # Load the dataset into a pandas DataFrame
#     df = pd.read_csv(dataset.file_path)
    
#     # Perform the operation
#     if operation == 'filter':
#         query_string = params.get('filter_condition')
#         df = df.query(query_string)
#     elif operation == 'sort':
#         sort_columns = params.get('sort_columns')
#         ascending = [True if order == "asc" else False for column, order in sort_columns]
#         df.sort_values(by=[column for column, order in sort_columns], ascending=ascending, inplace=True)
    
#     # Here you might want to save the transformed dataset, or return it directly
#     # For now, let's assume you return the transformed dataset as JSON
#     result = df.to_json(orient='records')
#     return result

# More endpoints for listing, updating, deleting datasets and performing other transformations go here


# @app.post("/users/register")
# async def register_user(username: str, email: str, password: str, db: Session = Depends(get_db)):
#     hashed_password = pwd_context.hash(password)
#     user = User(username=username, email=email, hashed_password=hashed_password)
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return {"username": user.username, "email": user.email}



from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import pandas as pd
from models import Dataset, engine, SessionLocal, Base
import shutil
import os

DATABASE_URL = "postgres://zhfycjmb:bdM-ujWF82U3oNrdwR2OyC1mKqj1oCjc@flora.db.elephantsql.com/zhfycjmb"
Base.metadata.create_all(bind=engine)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],   
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    headers = {
        'Access-Control-Allow-Origin': 'http://localhost:3000',
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Allow-Methods': '*',
        'Access-Control-Allow-Headers': '*',
    }
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=headers,
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    headers = {
        'Access-Control-Allow-Origin': 'http://localhost:3000',
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Allow-Methods': '*',
        'Access-Control-Allow-Headers': '*',
    }
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
        headers=headers,
    )

@app.post("/datasets/upload")
async def upload_dataset(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_location = f"uploads/{file.filename}"
    print('file', file_location)
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    
    try:
        df = pd.read_csv(file_location)  
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading dataset: {e}")

    dataset_dict = df.to_dict(orient='records')

    dataset = Dataset(name=file.filename, file_path=file_location)
    db.add(dataset)
    db.commit()
    db.refresh(dataset)

    return {"filename": dataset.name, "file_path": dataset.file_path, "dataset": dataset_dict, "dataset_id": dataset.dataset_id }

class FilterParameters(BaseModel):
    filter_condition: str

 
class TransformationInput(BaseModel):
    operation_type: str
    parameters: FilterParameters

@app.post("/datasets/{dataset_id}/transform")
async def transform_dataset(dataset_id: int, transformation_input: TransformationInput, db: Session = Depends(get_db)):
    dataset = db.query(Dataset).filter(Dataset.dataset_id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail=f"Dataset with ID {dataset_id} not found")
    
    try:
        df = pd.read_csv(dataset.file_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not load dataset from file path {dataset.file_path}: {e}")

    if transformation_input.operation_type == 'filter':
        filter_condition = transformation_input.parameters.filter_condition
        df = df.query(filter_condition)

    data = df.to_dict(orient='records')
    return data



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

