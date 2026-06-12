from ..schemas.product import ProductSchema, UpdateProductSchema;
from fastapi import APIRouter, Depends, HTTPException;
from ..helper.current_user import get_current_user;
from ..models.product import Product;
from sqlalchemy.orm import Session;
from app.config.db import getDB;
from ..models.user import User;

router = APIRouter(prefix="/product", tags=["Product"]);

@router.get("", summary="Get All Products")
def get_products(
    db: Session = Depends(getDB),
    current_user: User = Depends(get_current_user)
):

    products = (
        db.query(Product)
        .filter(Product.user_id == current_user.id)
        .all()
    );

    return products;

@router.post("", summary="Create New Product")
def create_product(
    data: ProductSchema,
    db: Session = Depends(getDB),
    current_user: User = Depends(get_current_user)
):

    product = Product(
        title=data.title,
        desc=data.desc,
        complete=data.complete,
        user_id=current_user.id
    );

    db.add(product);

    db.commit();

    db.refresh(product);

    return product;

@router.get("/{id}", summary="Get Product By ID")
def get_product(
    id: str,
    db: Session = Depends(getDB),
    current_user: User = Depends(get_current_user)
):

    product = (
        db.query(Product)
        .filter(
            Product.id == id,
            Product.user_id == current_user.id
        )
        .first()
    );

    if not product:

        raise HTTPException(
            status_code=404,
            detail="Product Not Found"
        )

    return product;

@router.put("/{id}", summary="Update Product By ID")
def update_product(
    id: str,
    data: UpdateProductSchema,
    db: Session = Depends(getDB),
    current_user: User = Depends(get_current_user)
):

    product = (
        db.query(Product)
        .filter(
            Product.id == id,
            Product.user_id == current_user.id
        )
        .first()
    );

    if not product:

        raise HTTPException(
            status_code=404,
            detail="Product Not Found"
        )

    if data.title is not None:

        product.title = data.title;

    if data.desc is not None:

        product.desc = data.desc;

    if data.complete is not None:

        product.complete = data.complete;

    db.commit();

    db.refresh(product);

    return product;

@router.delete("/{id}", summary="Delete Product By ID")
def delete_product(
    id: str,
    db: Session = Depends(getDB),
    current_user: User = Depends(get_current_user)
):

    product = (
        db.query(Product)
        .filter(
            Product.id == id,
            Product.user_id == current_user.id
        )
        .first()
    );

    if not product:

        raise HTTPException(
            status_code=404,
            detail="Product Not Found"
        );

    db.delete(product);

    db.commit();

    return {
        "success": True,
        "message": "Product Deleted Successfully"
    };