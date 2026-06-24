from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.dependencies import (
    get_db,
    get_current_user
)

from app.models.user import User

from app.schemas.order import (
    OrderResponse
)

from app.crud.order import (
    create_order
)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post(
    "/create",
    response_model=OrderResponse
)
def create_new_order(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    result = create_order(
        db,
        current_user.id
    )

    if not result:

        raise HTTPException(
            status_code=400,
            detail="Cart is empty"
        )

    if isinstance(result, dict):

        raise HTTPException(
            status_code=400,
            detail=result["error"]
        )

    return {
        "message":
        "Order created successfully",

        "order_id":
        result.id
    }