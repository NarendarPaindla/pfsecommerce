from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.category import Category


def create_product(
    db: Session,
    product_data
):

    category = (
        db.query(Category)
        .filter(
            Category.id ==
            product_data.category_id
        )
        .first()
    )

    if not category:
        return None

    product = Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        stock=product_data.stock,
        category_id=product_data.category_id
    )

    db.add(product)

    db.commit()

    db.refresh(product)

    return product


def get_products(
    db: Session
):
    return db.query(Product).all()


def get_product_by_id(
    db: Session,
    product_id: int
):
    return (
        db.query(Product)
        .filter(
            Product.id == product_id
        )
        .first()
    )


def update_product(
    db: Session,
    product_id: int,
    product_data
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

    product.name = product_data.name
    product.description = product_data.description
    product.price = product_data.price
    product.stock = product_data.stock
    product.category_id = (
        product_data.category_id
    )

    db.commit()

    db.refresh(product)

    return product


def delete_product(
    db: Session,
    product_id: int
):

    product = (
        db.query(Product)
        .filter(
            Product.id == product_id
        )
        .first()
    )

    if not product:
        return False

    db.delete(product)

    db.commit()

    return True

def update_product_image(
    db: Session,
    product_id: int,
    image_path: str
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

    product.image = image_path

    db.commit()

    db.refresh(product)

    return product