from sqlalchemy.orm import Session

from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.product import Product


def add_to_cart(
    db: Session,
    user_id: int,
    product_id: int,
    quantity: int
):

    product = (
        db.query(Product)
        .filter(
            Product.id == product_id
        )
        .first()
    )

    if not product:
        return None

    cart = (
        db.query(Cart)
        .filter(
            Cart.user_id == user_id
        )
        .first()
    )

    if not cart:

        cart = Cart(
            user_id=user_id
        )

        db.add(cart)

        db.commit()

        db.refresh(cart)

    cart_item = (
        db.query(CartItem)
        .filter(
            CartItem.cart_id == cart.id,
            CartItem.product_id == product_id
        )
        .first()
    )

    if cart_item:

        cart_item.quantity += quantity

    else:

        cart_item = CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity
        )

        db.add(cart_item)

    db.commit()

    return cart_item

def remove_from_cart(
    db: Session,
    user_id: int,
    cart_item_id: int
):

    cart = (
        db.query(Cart)
        .filter(
            Cart.user_id == user_id
        )
        .first()
    )

    if not cart:
        return False

    cart_item = (
        db.query(CartItem)
        .filter(
            CartItem.id == cart_item_id,
            CartItem.cart_id == cart.id
        )
        .first()
    )

    if not cart_item:
        return False

    db.delete(cart_item)

    db.commit()

    return True
def update_cart_quantity(
    db: Session,
    user_id: int,
    cart_item_id: int,
    quantity: int
):

    cart = (
        db.query(Cart)
        .filter(
            Cart.user_id == user_id
        )
        .first()
    )

    if not cart:
        return False

    cart_item = (
        db.query(CartItem)
        .filter(
            CartItem.id == cart_item_id,
            CartItem.cart_id == cart.id
        )
        .first()
    )

    if not cart_item:
        return False

    if quantity <= 0:

        db.delete(cart_item)

        db.commit()

        return "deleted"

    cart_item.quantity = quantity

    db.commit()

    return "updated"
def get_cart(
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
        return {
            "items": [],
            "grand_total": 0
        }

    cart_items = (
        db.query(CartItem)
        .filter(
            CartItem.cart_id == cart.id
        )
        .all()
    )

    items = []

    grand_total = 0

    for item in cart_items:

        product = (
            db.query(Product)
            .filter(
                Product.id ==
                item.product_id
            )
            .first()
        )

        item_total = (
            product.price
            * item.quantity
        )

        grand_total += item_total

        items.append(
            {
                "product_id":
                product.id,

                "product_name":
                product.name,

                "price":
                product.price,

                "quantity":
                item.quantity,

                "item_total":
                item_total
            }
        )

    return {
        "items": items,
        "grand_total": grand_total
    }