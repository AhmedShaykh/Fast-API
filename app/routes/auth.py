from app.config.utils import (hash_password, verify_password, create_token);
from ..schemas.user import (SignupSchema, SigninSchema, UpdateUserSchema);
from fastapi.security import (HTTPBearer, HTTPAuthorizationCredentials);
from fastapi import (APIRouter, Depends, HTTPException, status);
from ..helper.auth import (blacklist_token, is_blacklisted);
from ..helper.current_user import get_current_user;
from sqlalchemy.orm import Session;
from app.config.db import getDB;
from ..models.user import User;

router = APIRouter(prefix="/auth", tags=["Auth"]);

security = HTTPBearer();

@router.post("/signup", summary="Create New Account")
def signup(
    data: SignupSchema,
    db: Session = Depends(getDB)
):

    existing_user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    );

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="User Already Exists"
        );

    user = User(
        email=data.email,
        password=hash_password(data.password),
        fullname=data.fullname
    );

    db.add(user);

    db.commit();

    db.refresh(user);

    token = create_token({ "user_id": str(user.id) });

    return {
        "access_token": token,
        "user": {
            "id": user.id,
            "email": user.email,
            "fullname": user.fullname
        }
    };

@router.post("/signin", summary="Login Your Account")
def signin(
    data: SigninSchema,
    db: Session = Depends(getDB)
):

    user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    );

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid Credentials"
        );

    if not verify_password(data.password,user.password):

        raise HTTPException(
            status_code=401,
            detail="Invalid Credentials"
        );

    token = create_token({ "user_id": str(user.id) });

    return {
        "access_token": token,
        "user": {
            "id": user.id,
            "email": user.email,
            "fullname": user.fullname,
            "created": user.created
        }
    };

@router.get("/user", summary="Get Your Account")
def get_user(current_user: User = Depends(get_current_user)):

    return {
        "id": current_user.id,
        "email": current_user.email,
        "fullname": current_user.fullname
    };

@router.put("/user", summary="Update Your Account")
def update_user(
    data: UpdateUserSchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(getDB)
):

    if data.email is not None:

        current_user.email = data.email;

    if data.fullname is not None:

        current_user.fullname = data.fullname;

    if data.password is not None:

        current_user.password = hash_password(data.password);

    db.commit();

    db.refresh(current_user);

    return {
        "msg": "User Updated Successfully",
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "fullname": current_user.fullname
        }
    };

@router.post("/logout", summary="Log Out Your Account")
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(getDB)
):

    token = credentials.credentials;

    if is_blacklisted(db, token):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You Are Already Logged Out"
        );

    blacklist_token(db, token);

    return { "msg": "User Logged Out Successfully" };