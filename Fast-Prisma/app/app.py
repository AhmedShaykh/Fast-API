from fastapi.exceptions import RequestValidationError;
from app.config.db import connect_db, disconnect_db;
from fastapi.middleware.cors import CORSMiddleware;
from fastapi.responses import JSONResponse;
from app.routes import auth, product;
from fastapi import FastAPI;

app = FastAPI(
    title="Full Stack Fast API",
    description="Full Stack Fast Authentication Rest APIs With Prisma ORM",
    version="1.0.0"
);

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
);

@app.on_event("startup")
async def startup():

    await connect_db();

@app.on_event("shutdown")
async def shutdown():

    await disconnect_db();

app.include_router(auth.router, prefix="/api");

app.include_router(product.router, prefix="/api");

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):

    errors = {};

    for error in exc.errors():

        field = error["loc"][-1];

        errors[field] = error["msg"];

    return JSONResponse(
        status_code=422,
        content={
            "message": "Validation Error",
            "errors": errors
        }
    );