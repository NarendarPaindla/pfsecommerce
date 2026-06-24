from sqlalchemy.orm import Session

from app.models.cart import Cart
from app.models.cart_item import CartItem

from app.models.order import Order
from app.models.order_item import OrderItem

from app.models.product import Product


def create_order(
    db: Session,
    user_id: int
):

    cart = (
        db.query(Cart)
        .filter(
            Cart.user_id == user_id
        )
        .first()
    )

    if not cart:
        return None

    cart_items = (
        db.query(CartItem)
        .filter(
            CartItem.cart_id == cart.id
        )
        .all()
    )

    if not cart_items:
        return None

    for item in cart_items:

        product = (
            db.query(Product)
            .filter(
                Product.id ==
                item.product_id
            )
            .first()
        )

        if (
            product.stock
            < item.quantity
        ):
            return {
                "error":
                f"Insufficient stock for {product.name}"
            }

    order = Order(
        user_id=user_id
    )

    db.add(order)

    db.commit()

    db.refresh(order)

    for item in cart_items:

        product = (
            db.query(Product)
            .filter(
                Product.id ==
                item.product_id
            )
            .first()
        )

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            price=product.price
        )

        db.add(order_item)

        product.stock -= item.quantity

    db.commit()

    for item in cart_items:

        db.delete(item)

    db.commit()

    return order

def get_order_history(
    db: Session,
    user_id: int
):

    orders = (
        db.query(Order)
        .filter(
            Order.user_id == user_id
        )
        .all()
    )

    response = []

    for order in orders:

        order_items = (
            db.query(OrderItem)
            .filter(
                OrderItem.order_id
                == order.id
            )
            .all()
        )

        items = []

        total_amount = 0

        for item in order_items:

            product = (
                db.query(Product)
                .filter(
                    Product.id ==
                    item.product_id
                )
                .first()
            )

            item_total = (
                item.price
                * item.quantity
            )

            total_amount += item_total

            items.append(
                {
                    "product_name":
                    product.name,

                    "quantity":
                    item.quantity,

                    "price":
                    item.price,

                    "total":
                    item_total
                }
            )

        response.append(
            {
                "order_id":
                order.id,

                "total_amount":
                total_amount,

                "items":
                items
            }
        )

    return response

def get_all_orders(
    db: Session
):

    return (
        db.query(Order)
        .all()
    )

def update_order_status(
    db: Session,
    order_id: int,
    status: str
):

    order = (
        db.query(Order)
        .filter(
            Order.id == order_id
        )
        .first()
    )

    if not order:
        return None

    order.status = status

    db.commit()

    db.refresh(order)

    return order