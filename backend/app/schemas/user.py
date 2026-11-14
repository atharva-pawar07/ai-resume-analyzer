
from pydantic import BaseModel, EmailStr, Field, ConfigDict


# Data required when registering a new user
class UserCreate(BaseModel):
    full_name: str = Field(
        min_length=2,
        max_length=100
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128
    )


# Data required when logging in
class UserLogin(BaseModel):
    email: EmailStr

    password: str


# Data returned to the client
class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


# JWT token response
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
