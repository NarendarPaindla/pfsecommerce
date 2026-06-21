from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    description = Column(
        String,
        nullable=True
    )

    price = Column(
        Float,
        nullable=False
    )

    stock = Column(
        Integer,
        default=0
    )

    image = Column(
        String,
        nullable=True
    )

    category_id = Column(
        Integer,
        ForeignKey("categories.id")
    )