from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Memory

async def get_memories_by_client(
    db,
    client_id,
    limit=5
):

    stmt = (
        select(Memory)
        .where(
            Memory.client_id == client_id
        )
        .order_by(
            Memory.created_at.desc()
        )
        .limit(limit)
    )


    result = await db.execute(stmt)

    return result.scalars().all()

async def create_memory(
    db: AsyncSession,
    client_id: UUID,
    session_id: UUID,
    content: str,
    memory_type: str,
    importance_score: float,
    embedding=None,
    rule_id=None
):
    
    memory = Memory(
        client_id=client_id,
        session_id=session_id,
        content=content,
        memory_type=memory_type,
        importance_score=importance_score,
        embedding=embedding,
        rule_id=rule_id
    )

    db.add(memory)

    await db.commit()
    await db.refresh(memory)

    return memory

async def get_memories_by_client(
    db: AsyncSession,
    client_id: UUID,
    limit: int = 5
):
    stmt = (
        select(Memory)
        .where(Memory.client_id == client_id)
        .order_by(Memory.importance_score.desc())
        .limit(limit)
    )

    result = await db.execute(stmt)

    return result.scalars().all()