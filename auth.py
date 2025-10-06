from datetime import datetime, timedelta, timezone
from typing import Optional
from pydantic import BaseModel

from fastapi import FastAPI, APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

import hashlib

app = FastAPI()
router = APIRouter(prefix="/auth", tags=["Authentication"])


class User(BaseModel):
    username: str
    password: str

# Secret key for JWT encoding/decoding
SECRET_KEY = "6EKPVNR_4STFSkzDhJjwVcc9ggh5ZgwHSFHDG33ZsBa9osJxr_Gv1cPJ-M3DKnM0K7GV-xHmt1SdAlWFXXQC-Q"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Dummy user database
users_db = {}
def verify_password(plain_password, hashed_password):
    sha_password = hashlib.sha256(plain_password.encode()).hexdigest()
    return pwd_context.verify(sha_password, hashed_password)

def get_password_hash(password):
    sha_password = hashlib.sha256(password.encode()).hexdigest()
    return pwd_context.hash(sha_password)
def creat_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Register route
@router.post("/register")
def register(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    users_db[user.username] = {
        "username": user.username,
        "hashed_password": get_password_hash(user.password),
        }
    return {"message": "User created successfully"}

# Login route
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = creat_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Protected route
@router.get("/me")
def read_users_me(token: str = Depends(oauth2_scheme)):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None or username not in users_db:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return {"username": username}
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")