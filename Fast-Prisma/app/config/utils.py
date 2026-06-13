from datetime import datetime, timedelta, UTC;
from passlib.context import CryptContext;
from dotenv import load_dotenv;
from jose import jwt, JWTError;
import os;

load_dotenv();

SECRET_KEY = os.getenv("SECRET_KEY");

ALGORITHM = os.getenv("ALGORITHM");

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto");

def hash_password(password: str):

    return pwd_context.hash(password);

def verify_password(plain: str, hashed: str):

    return pwd_context.verify(plain, hashed);

def create_token(data: dict, expires_minutes: int = 60):

    payload = data.copy();

    payload["exp"] = (datetime.now(UTC) + timedelta(minutes=expires_minutes));

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    );

def decode_token(token: str):

    try:

        return jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        );

    except JWTError:

        return None;