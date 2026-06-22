from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

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
    delete_product
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