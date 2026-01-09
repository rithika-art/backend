from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from models import User
from jose import JWTError, jwt
from auth.jwt_utils import(
    create_access_token,
    create_refresh_token,
    SECRET_KEY,
    ALGORITHM
)
from auth_utils import hash_password

router = APIRouter(
    prefix="/auth",tags=["Auth"]
)


class RegisterIn(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str 

class RefreshRequest(BaseModel):
    refresh_token: str 

@router.post("/login")
def login(data: LoginRequest):
    fake_user_id = 1
    access_token = create_access_token(data={"user_id": fake_user_id})
    refresh_token = create_refresh_token(data={"user_id": fake_user_id})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
@router.post("/refresh")
def refresh_token(data: RefreshRequest):
    try:
        payload = jwt.decode(
            data.refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id=payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401,detail="INVALID TOKEN")
        new_access_token=create_access_token(
            {"user_id":user_id}
        )
        return{
            "access_token": new_access_token,
            "token_type": "bearer"
        }
    except JWTError:
        raise HTTPException(status_code=401,detail="INVALID REFRESH TOKEN")


@router.post("/api/v1/auth/register")
async def register(email: str, password: str, db: Session = Depends(get_db)):
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Hash the password
        hashed_password = hash_password(password)
        
        # Create new user
        new_user = User(
            email=email,
            password=hashed_password
        )
        
        # Add to database
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return {
            "id": new_user.id,
            "email": new_user.email,
            "message": "User registered successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")
