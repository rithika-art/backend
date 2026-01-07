from fastapi import APIRouter
from pydantic import BaseModel
from auth_utils import hash_password

router = APIRouter()


class RegisterIn(BaseModel):
    name:str
    email:str
    password:str

@router.post("/register")
def register(data: RegisterIn):
    hashed=hash_password(data.password)
    return {
        "name":data.name,
        "email":data.email,
        "password":data.password
    }

