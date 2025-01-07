from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from services.user_service import UserService
from core.database import get_db
from core.logging import logger
from pydantic import BaseModel, EmailStr

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={
        400: {"description": "Bad Request"},
        500: {"description": "Internal Server Error"},
    },
)


class UserCreate(BaseModel):
    email: EmailStr
    name: str

    class Config:
        json_schema_extra = {
            "example": {"email": "user@example.com", "name": "John Doe"}
        }


@router.post("")
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        user_service = UserService(db)
        user = await user_service.create_user(
            email=user_data.email, name=user_data.name
        )
        return {
            "message": "User created successfully",
            "user_id": user.id,
            "email": user.email,
            "name": user.name,
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creating user")
