from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Tag
from src.schemas import TagModel

async def get_tags(skip: int, limit: int, db: AsyncSession) -> List[Tag]:
    query = select(Tag).offset(skip).limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())

async def get_tag(tag_id: int, db: AsyncSession) -> Tag | None:
    query = select(Tag).filter(Tag.id == tag_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def create_tag(body: TagModel, db: AsyncSession) -> Tag: # Виправлено кому на двокрапку
    tag = Tag(name=body.name)
    db.add(tag)
    await db.commit()   # Додано await
    await db.refresh(tag) # Додано await
    return tag

async def update_tag(tag_id: int, body: TagModel, db: AsyncSession) -> Tag | None:
    tag = await get_tag(tag_id, db) # Використовуємо вже готову асинхронну функцію пошуку
    if tag:
        tag.name = body.name
        await db.commit() # Додано await
        await db.refresh(tag)
    return tag

async def remove_tag(tag_id: int, db: AsyncSession) -> Tag | None:
    tag = await get_tag(tag_id, db)
    if tag:
        await db.delete(tag) # Додано await для видалення в асинхронній сесії
        await db.commit()    # Додано await
    return tag
