from pydantic import BaseModel


class OrderResponse(
    BaseModel
):
    message: str
    order_id: int


class OrderItemHistory(
    BaseModel
):
    product_name: str
    quantity: int
    price: float
    total: float


class OrderHistoryItem(
    BaseModel
):
    order_id: int
    status: str
    total_amount: float
    items: list[OrderItemHistory]

class UpdateOrderStatusRequest(
    BaseModel
):
    status: str