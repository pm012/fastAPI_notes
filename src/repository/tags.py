from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Tag
from src.schemas import TagModel

async def get_tags(skip: int, limit: int, db: AsyncSession) -> List[Tag]:
    return db.query(Tag).offset(skip).limit(limit).all()

async def get_tag(tag_id: int, db: AsyncSession) -> Tag:
    return db.query(Tag).filter(Tag.id==tag_id).first()

async def create_tag(body, TagModel, db: AsyncSession) -> Tag:
    tag = Tag(name=body.name)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag

async def update_tag(tag_id: int, body: TagModel, db: AsyncSession)->Tag | None:
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        tag.name = body.name
        db.commit()
        return tag
    
    
async def remove_tag(tag_id: int, db: AsyncSession) -> Tag | None:
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        db.delete(tag)
        db.commit()
    return tag