from ..schemas.product import ProductSchema, UpdateProductSchema;
from fastapi import APIRouter, Depends, HTTPException;
from ..helper.current_user import get_current_user;
from app.config.db import db;

router = APIRouter(prefix="/product", tags=["Product"]);

@router.get("", summary="Get All Products")
async def get_products(current_user=Depends(get_current_user)):

    products = await db.product.find_many(where={"user_id": current_user.id});

    return products;

@router.post("", summary="Create New Product")
async def create_product(
    data: ProductSchema,
    current_user=Depends(get_current_user)
):

    product = await db.product.create(data={
        "title": data.title,
        "desc": data.desc,
        "price": data.price,
        "user_id": current_user.id
    });

    return product;

@router.get("/{id}", summary="Get Product By ID")
async def get_product(id: str, current_user=Depends(get_current_user)):

    product = await db.product.find_first(where={
        "id": id,
        "user_id": current_user.id
    });

    if not product:

        raise HTTPException(status_code=404, detail="Product Not Found");

    return product;

@router.put("/{id}", summary="Update Product By ID")
async def update_product(
    id: str,
    data: UpdateProductSchema,
    current_user=Depends(get_current_user)
):

    product = await db.product.find_first(where={
        "id": id,
        "user_id": current_user.id
    });

    if not product:

        raise HTTPException(status_code=404, detail="Product Not Found");

    update_data = {};

    if data.title is not None:

        update_data["title"] = data.title;

    if data.desc is not None:

        update_data["desc"] = data.desc;

    if data.price is not None:

        update_data["price"] = data.price;

    updated_product = await db.product.update(
        where={"id": id},
        data=update_data
    );

    return updated_product;

@router.delete("/{id}", summary="Delete Product By ID")
async def delete_product(id: str, current_user=Depends(get_current_user)):

    product = await db.product.find_first(where={
        "id": id,
        "user_id": current_user.id
    });

    if not product:

        raise HTTPException(status_code=404, detail="Product Not Found");

    await db.product.delete(where={"id": id});

    return {
        "success": True,
        "message": "Product Deleted Successfully"
    };