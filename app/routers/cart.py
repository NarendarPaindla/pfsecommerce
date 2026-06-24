from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException


from sqlalchemy.orm import Session

from app.dependencies import (
    get_db,
    get_current_user
)

from app.models.user import User

from app.schemas.cart import (
    AddToCartRequest,
    CartMessageResponse,
    UpdateCartQuantityRequest,
     CartResponse
)

from app.crud.cart import (
    add_to_cart,
     remove_from_cart,
      update_cart_quantity,
       get_cart
)





router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)


@router.post(
    "/add",
    response_model=CartMessageResponse
)
def add_product_to_cart(
    request: AddToCartRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    item = add_to_cart(
        db=db,
        user_id=current_user.id,
        product_id=request.product_id,
        quantity=request.quantity
    )

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return {
        "message":
        "Product added to cart"
    }

@router.delete(
    "/remove/{cart_item_id}",
    response_model=CartMessageResponse
)
def remove_product_from_cart(
    cart_item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    deleted = remove_from_cart(
        db=db,
        user_id=current_user.id,
        cart_item_id=cart_item_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Cart item not found"
        )

    return {
        "message":
        "Product removed from cart"
    }

@router.put(
    "/update/{cart_item_id}",
    response_model=
    CartMessageResponse
)
def update_quantity(
    cart_item_id: int,
    request:
    UpdateCartQuantityRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    result = update_cart_quantity(
        db=db,
        user_id=current_user.id,
        cart_item_id=cart_item_id,
        quantity=request.quantity
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Cart item not found"
        )

    if result == "deleted":

        return {
            "message":
            "Cart item removed"
        }

    return {
        "message":
        "Cart quantity updated"
    }

@router.get(
    "/",
    response_model=CartResponse
)
def view_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    return get_cart(
        db,
        current_user.id
    )