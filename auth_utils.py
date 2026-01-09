from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    # Make sure you're encoding properly
    hashed = pwd_context.hash(password.encode('utf-8')[:72].decode('utf-8'))
    return hashed

def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)
