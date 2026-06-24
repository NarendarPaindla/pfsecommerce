from pydantic import BaseModel


class AddToCartRequest(
    BaseModel
):
    product_id: int
    quantity: int = 1


class UpdateCartQuantityRequest(
    BaseModel
):
    quantity: int


class CartMessageResponse(
    BaseModel
):
    message: str


class CartItemResponse(
    BaseModel
):
    product_id: int
    product_name: str
    price: float
    quantity: int
    item_total: float


class CartResponse(
    BaseModel
):
    items: list[CartItemResponse]
    grand_total: float