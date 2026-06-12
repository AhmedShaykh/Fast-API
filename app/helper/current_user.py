from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials;
from fastapi import Depends, HTTPException;
from app.config.utils import decode_token;
from ..helper.auth import is_blacklisted;
from sqlalchemy.orm import Session;
from app.config.db import getDB;
from ..models.user import User;

security = HTTPBearer();

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(getDB)
):

    token = credentials.credentials;

    if is_blacklisted(db, token):

        raise HTTPException(
            status_code=401,
            detail="Token Has Been Logged Out"
        );

    payload = decode_token(token);

    user_id = payload.get("user_id");

    if not user_id:

        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        );

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    );

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User Not Found"
        );

    return user;