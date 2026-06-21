from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.schemas.user import UserCreate
from app.schemas.user import UserResponse

from app.crud.user import create_user
from fastapi import HTTPException
from app.core.security import create_access_token
from app.schemas.user import TokenResponse
from app.schemas.user import (
    UserLogin,
    LoginResponse
)
from app.schemas.user import UserUpdate

from app.crud.user import (
    get_users,
    get_user_by_id,
    update_user,
    delete_user
)
from app.crud.user import (
    authenticate_user
)

from app.dependencies import get_current_user

from app.models.user import User
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/register",
    response_model=UserResponse
)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return create_user(
        db=db,
        user=user
    )

@router.post(
    "/login",
    response_model=TokenResponse
)
def login_user(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):

    user = authenticate_user(
        db=db,
        email=credentials.email,
        password=credentials.password
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={
            "sub": user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/me")
def get_me(
    current_user: User = Depends(
        get_current_user
    )
):

    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role
    }

@router.get(
    "/",
    response_model=list[UserResponse]
)
def get_all_users(
    db: Session = Depends(get_db)
):

    return get_users(db)

@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_single_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = get_user_by_id(
        db,
        user_id
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user
@router.put(
    "/{user_id}",
    response_model=UserResponse
)
def update_single_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):

    user = update_user(
        db=db,
        user_id=user_id,
        name=user_data.name,
        email=user_data.email
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.delete("/{user_id}")
def remove_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    deleted = delete_user(
        db,
        user_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "User deleted successfully"
    }