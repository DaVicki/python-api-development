from passlib.context import CryptContext

# setup password context from CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)