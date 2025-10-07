from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from pydantic import BaseModel, constr

from database import SessionLocal
from models import User
from fastapi.security import OAuth2PasswordBearer

# Pydantic schemas 
class UserCreate(BaseModel):
    username: str
    password: constr(min_length=6, max_length=72)

class UserLogin(BaseModel):
    username: str
    password: constr(min_length=6, max_length=72)

# Router
router = APIRouter(prefix="/auth", tags=["Authentication"])

# JWT settings
SECRET_KEY = "6EKPVNR_4STFSkzDhJjwVcc9ggh5ZgwHSFHDG33ZsBa9osJxr_Gv1cPJ-M3DKnM0K7GV-xHmt1SdAlWFXXQC-Q"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Password verification and hashing
def get_password_hash(password: str):
    if not password:
        raise ValueError("Password cannot be empty")
    truncated = password[:72]  # bcrypt limit
    return pwd_context.hash(truncated)

def verify_password(plain_password: str, hashed_password: str):
    truncated = plain_password[:72]
    return pwd_context.verify(truncated, hashed_password)

# JWT token creation
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Routes
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Decoded payload:", payload)
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return {"username": user.username}
    
    except JWTError as e:
        print("JWTError:", e)
        raise HTTPException(status_code=401, detail="Could not validate credentials")
