from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user import User
from core.logging import logger
from fastapi import HTTPException
from uuid import UUID


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, email: str, name: str) -> User:
        try:
            query = select(User).filter(User.email == email)
            result = await self.db.execute(query)
            existing_user = result.scalar_one_or_none()

            if existing_user:
                logger.error(f"Attempted to create user with existing email: {email}")
                raise HTTPException(status_code=400, detail="Email already registered")

            user = User(email=email, name=name)
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)

            logger.info(f"Created new user: {email}")
            return user

        except HTTPException:
            await self.db.rollback()
            raise

        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error creating user: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")
