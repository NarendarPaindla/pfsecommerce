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