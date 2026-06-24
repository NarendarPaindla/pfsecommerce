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