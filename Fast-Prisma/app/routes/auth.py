from app.config.utils import hash_password, verify_password, create_token;
from ..schemas.user import SignupSchema, SigninSchema, UpdateUserSchema;
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials;
from fastapi import APIRouter, Depends, HTTPException, status;
from ..helper.auth import blacklist_token, is_blacklisted;
from ..helper.current_user import get_current_user;
from app.config.db import db;

router = APIRouter(prefix="/auth", tags=["Auth"]);

security = HTTPBearer();

@router.post("/signup", summary="Create New Account")
async def signup(data: SignupSchema):

    existing_user = await db.user.find_unique(where={"email": data.email});

    if existing_user:

        raise HTTPException(status_code=400, detail="User Already Exists");

    user = await db.user.create(data={
        "email": data.email,
        "password": hash_password(data.password),
        "fullname": data.fullname
    });

    token = create_token({"user_id": user.id});

    return {
        "access_token": token,
        "user": {
            "id": user.id,
            "email": user.email,
            "fullname": user.fullname
        }
    };

@router.post("/signin", summary="Login Your Account")
async def signin(data: SigninSchema):

    user = await db.user.find_unique(where={"email": data.email});

    if not user or not verify_password(data.password, user.password):

        raise HTTPException(status_code=401, detail="Invalid Credentials");

    token = create_token({"user_id": user.id});

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
async def get_user(current_user=Depends(get_current_user)):

    return {
        "id": current_user.id,
        "email": current_user.email,
        "fullname": current_user.fullname
    };

@router.put("/user", summary="Update Your Account")
async def update_user(
    data: UpdateUserSchema,
    current_user=Depends(get_current_user)
):

    update_data = {};

    if data.email is not None:

        existing_user = await db.user.find_unique(
            where={"email": data.email}
        );

        if (existing_user and existing_user.id != current_user.id):

            raise HTTPException(
                status_code=400,
                detail="Email Already Exists"
            );

        update_data["email"] = data.email;

    if data.fullname is not None:

        update_data["fullname"] = data.fullname;

    if data.password is not None:

        update_data["password"] = hash_password(data.password);

    updated_user = await db.user.update(
        where={"id": current_user.id},
        data=update_data
    );

    return {
        "msg": "User Updated Successfully",
        "user": {
            "id": updated_user.id,
            "email": updated_user.email,
            "fullname": updated_user.fullname
        }
    };

@router.post("/logout", summary="Log Out Your Account")
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):

    token = credentials.credentials;

    if await is_blacklisted(token):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You Are Already Logged Out"
        );

    await blacklist_token(token);

    return {"msg": "User Logged Out Successfully"};