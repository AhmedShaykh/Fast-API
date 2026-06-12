from fastapi.exceptions import RequestValidationError;
from fastapi.middleware.cors import CORSMiddleware;
from fastapi.responses import JSONResponse;
from app.config.db import Base, engine;
from app.routes import auth, product;
from fastapi import FastAPI;
from mangum import Mangum;

Base.metadata.create_all(bind=engine);

app = FastAPI(
    title="Full Stack Fast API",
    description="Full Stack Fast Authentication Rest APIs With SQLAlchmey",
    version="1.0.0"
);

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
);

handler = Mangum(app); # For AWS Lambda

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