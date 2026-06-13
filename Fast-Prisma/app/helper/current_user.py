from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials;
from fastapi import Depends, HTTPException;
from app.helper.auth import is_blacklisted;
from app.config.utils import decode_token;
from app.config.db import db;

security = HTTPBearer();

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):

    token = credentials.credentials;

    blacklisted = await is_blacklisted(token);

    if blacklisted:

        raise HTTPException(
            status_code=401,
            detail="Token Has Been Logged Out"
        );

    payload = decode_token(token);

    if not payload:

        raise HTTPException(
            status_code=401,
            detail="Invalid Or Expired Token"
        );

    user_id = payload.get("user_id");

    if not user_id:

        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        );

    user = await db.user.find_unique(
        where={"id": user_id}
    );

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User Not Found"
        );

    return user;