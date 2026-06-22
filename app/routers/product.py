from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
import os

from uuid import uuid4

from fastapi import UploadFile
from fastapi import File
from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.core.permissions import (
    require_admin
)

from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse
)

from app.crud.product import (
    create_product,
    get_products,
    get_product_by_id,
    update_product,
    delete_product,
    update_product_image
)
from app.crud.product import (
    search_products
)

from app.crud.product import (
    filter_products
)
router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post(
    "/",
    response_model=ProductResponse
)
def create_new_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):

    created = create_product(
        db,
        product
    )

    if not created:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return created


@router.get(
    "/",
    response_model=list[ProductResponse]
)
def list_products(
    db: Session = Depends(get_db)
):
    return get_products(db)

@router.get(
    "/search/",
    response_model=list[ProductResponse]
)
def search_product_list(
    q: str,
    db: Session = Depends(get_db)
):

    return search_products(
        db,
        q
    )


@router.get(
    "/filter/",
    response_model=list[ProductResponse]
)
def filter_product_list(
    category_id: int | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    db: Session = Depends(get_db)
):

    return filter_products(
        db=db,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price
    )

@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
def get_single_product(
    product_id: int,
    db: Session = Depends(get_db)
):

    product = get_product_by_id(
        db,
        product_id
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


@router.put(
    "/{product_id}",
    response_model=ProductResponse
)
def update_existing_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):

    updated = update_product(
        db,
        product_id,
        product
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return updated


@router.delete(
    "/{product_id}"
)
def remove_product(
    product_id: int,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):

    deleted = delete_product(
        db,
        product_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return {
        "message":
        "Product deleted successfully"
    }

@router.post(
    "/{product_id}/upload-image"
)
def upload_product_image(
    product_id: int,
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):

    product = get_product_by_id(
        db,
        product_id
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    extension = image.filename.split(".")[-1]

    filename = (
        f"{uuid4()}.{extension}"
    )

    file_path = (
        f"uploads/products/{filename}"
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        buffer.write(
            image.file.read()
        )

    updated_product = (
        update_product_image(
            db,
            product_id,
            file_path
        )
    )

    return {
        "message":
        "Image uploaded successfully",

        "image_path":
        updated_product.image
    }