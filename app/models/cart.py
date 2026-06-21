from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from app.database import Base


class Cart(Base):
    __tablename__ = "carts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )