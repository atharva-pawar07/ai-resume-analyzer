
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_db
from backend.app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)
from backend.app.models.user import User
from backend.app.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
    TokenResponse
)


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)


# User registration
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    # Check whether email already exists
    result = await db.execute(
        select(User).where(User.email == user_data.email)
    )

    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered"
        )

    # Hash the password before saving
    new_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )

    db.add(new_user)

    try:
        await db.commit()
        await db.refresh(new_user)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered"
        )

    return new_user


# User login
@router.post(
    "/login",
    response_model=TokenResponse
)
async def login_user(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.email == login_data.email)
    )

    user = result.scalar_one_or_none()

    # Verify email and password
    if not user or not verify_password(
        login_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Create JWT token
    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
