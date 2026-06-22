from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    category_id: int


class ProductUpdate(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    category_id: int


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock: int
    image: str | None
    category_id: int

    model_config = {
        "from_attributes": True
    }

class ProductPaginationResponse(
    BaseModel
):
    total: int
    page: int
    size: int
    data: list[ProductResponse]