from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.core.permissions import (
    require_admin
)

from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse
)

from app.crud.category import (
    create_category,
    get_categories,
    get_category_by_id,
    update_category,
    delete_category
)

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.post(
    "/",
    response_model=CategoryResponse
)
def create_new_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    return create_category(
        db,
        category.name
    )


@router.get(
    "/",
    response_model=list[CategoryResponse]
)
def list_categories(
    db: Session = Depends(get_db)
):
    return get_categories(db)


@router.get(
    "/{category_id}",
    response_model=CategoryResponse
)
def get_category(
    category_id: int,
    db: Session = Depends(get_db)
):

    category = get_category_by_id(
        db,
        category_id
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return category


@router.put(
    "/{category_id}",
    response_model=CategoryResponse
)
def update_existing_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):

    updated = update_category(
        db,
        category_id,
        category.name
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return updated


@router.delete(
    "/{category_id}"
)
def remove_category(
    category_id: int,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):

    deleted = delete_category(
        db,
        category_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return {
        "message":
        "Category deleted successfully"
    }