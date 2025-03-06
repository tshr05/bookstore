from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import SQLModel, Session, select
from passlib.context import CryptContext

from bookstore.bookmgmt import router as book_router
from bookstore.database import get_db, engine  # ✅ Keep it clean
from bookstore.utils import create_access_token
from bookstore.models import User  # Assuming User is a SQLModel
from bookstore.schemas import UserCreate, UserResponse  # Pydantic schemas

app = FastAPI()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Include Books API
app.include_router(book_router, tags=["Books"])

# Ensure database tables are created
@app.on_event("startup")
def create_tables():
    SQLModel.metadata.create_all(engine)

@app.get("/health")
async def get_health():
    """Health check endpoint"""
    return {"status": "up"}

@app.post("/signup", response_model=UserResponse)
async def create_user_signup(user_credentials: UserCreate, db: Session = Depends(get_db)):
    """Registers a new user"""
    statement = select(User).where(User.email == user_credentials.email)
    existing_user = db.execute(statement).scalar_one_or_none()  # ✅ Fixed exec() usage
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(user_credentials.password)
    new_user = User(email=user_credentials.email, password=hashed_password)

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")

@app.post("/login")
async def login_for_access_token(user_credentials: UserCreate, db: Session = Depends(get_db)):
    """Authenticates user and returns a JWT token"""
    statement = select(User).where(User.email == user_credentials.email)
    user = db.execute(statement).scalar_one_or_none()  # ✅ Fixed exec() usage
    
    if not user or not pwd_context.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}
