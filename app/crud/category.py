from sqlalchemy.orm import Session

from app.models.category import Category


def create_category(
    db: Session,
    name: str
):

    category = Category(
        name=name
    )

    db.add(category)

    db.commit()

    db.refresh(category)

    return category


def get_categories(
    db: Session
):
    return db.query(
        Category
    ).all()


def get_category_by_id(
    db: Session,
    category_id: int
):

    return (
        db.query(Category)
        .filter(
            Category.id == category_id
        )
        .first()
    )


def update_category(
    db: Session,
    category_id: int,
    name: str
):

    category = (
        db.query(Category)
        .filter(
            Category.id == category_id
        )
        .first()
    )

    if not category:
        return None

    category.name = name

    db.commit()

    db.refresh(category)

    return category


def delete_category(
    db: Session,
    category_id: int
):

    category = (
        db.query(Category)
        .filter(
            Category.id == category_id
        )
        .first()
    )

    if not category:
        return False

    db.delete(category)

    db.commit()

    return True