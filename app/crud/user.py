from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.models import User, ClientProfile 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def get_user_by_phone(db: AsyncSession, phone_number: str) -> User | None:
    result = await db.execute(select(User).where(User.phone_number == phone_number))
    return result.scalars().first()

async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().first()

"""
async def create_user(db: AsyncSession, phone_number: str, role: str = "CLIENT") -> User:
    db_user = User(
        phone_number=phone_number,
        role=role,
        is_active=True
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
"""
async def get_or_create_user(db: AsyncSession, phone_number: str) -> User:
    # 1. Check if user exists
    result = await db.execute(select(User).where(User.phone_number == phone_number))
    user = result.scalars().first()

    if user:
        return user

    # 2. If user does not exist, create User
    new_user = User(
        phone_number=phone_number,
        role="CLIENT",
        is_active=True
    )
    db.add(new_user)
    await db.flush() # flush() gets the new_user.id without committing the transaction yet

    # 3. Create the corresponding ClientProfile
    #new_profile = ClientProfile(id=new_user.id) # Or however your relation is set up

    # 3. Create the corresponding ClientProfile
    # Fix: Explicitly set user_id
    new_profile = ClientProfile(user_id=new_user.id) 
    
    db.add(new_profile)

    # 4. Commit both to the database
    await db.commit()
    await db.refresh(new_user)
    
    return new_user


async def get_or_create_user1(db: AsyncSession, phone_number: str) -> User:
    """
    Finds a user by phone number or creates a new one along with a ClientProfile.
    """
    result = await db.execute(select(User).filter(User.phone_number == phone_number))
    user = result.scalar_one_or_none()

    if not user:
        # Create new user
        user = User(
            phone_number=phone_number,
            role="client"  # Or use your Enum if you have one
        )
        db.add(user)
        await db.flush()  # Generates user.id without committing yet

        # Create associated client profile
        client_profile = ClientProfile(id=user.id) # Assuming ClientProfile.id is the foreign key to User.id based on your previous models
        db.add(client_profile)

        await db.commit()
        await db.refresh(user)

    return user

