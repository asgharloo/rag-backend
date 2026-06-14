from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.models import User, ClientProfile
from uuid import UUID
from app.models.models import UserRole


async def get_user_by_phone(db: AsyncSession, phone_number: str):
    result = await db.execute(
        select(User).where(User.phone_number == phone_number)
    )
    return result.scalars().first()


async def get_user_by_id(db: AsyncSession, user_id: UUID):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalars().first()


async def get_or_create_user(db: AsyncSession, phone_number: str):
    result = await db.execute(
        select(User).where(User.phone_number == phone_number)
    )
    user = result.scalars().first()

    if user:
        return user

    user = User(
        phone_number=phone_number,
        role=UserRole.CLIENT.value,
        is_active=True
    )

    db.add(user)
    await db.flush()

    profile = ClientProfile(user_id=user.id)
    db.add(profile)

    await db.commit()
    await db.refresh(user)

    return user