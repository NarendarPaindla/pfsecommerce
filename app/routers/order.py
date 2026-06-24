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
    OrderResponse,
     OrderHistoryItem,
     UpdateOrderStatusRequest
)

from app.crud.order import (
    create_order,
    get_order_history,
     get_all_orders,
    update_order_status
)

from app.core.permissions import (
    require_admin
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

@router.get(
    "/history",
    response_model=
    list[OrderHistoryItem]
)
def order_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    return get_order_history(
        db,
        current_user.id
    )
@router.get(
    "/admin/all"
)
def admin_all_orders(
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):

    return get_all_orders(db)

@router.put(
    "/admin/status/{order_id}"
)
def admin_update_status(
    order_id: int,
    request:
    UpdateOrderStatusRequest,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):

    order = update_order_status(
        db,
        order_id,
        request.status
    )

    if not order:

        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return {
        "message":
        "Order status updated",

        "status":
        order.status
    }