from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Note, Tag
from src.schemas import NoteModel, NoteUpdate, NoteStatusUpdate

async def get_notes(skip: int, limit: int, db: AsyncSession) -> List[Note]:
    query = select(Note).offset(skip).limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())

async def get_note(note_id: int, db: AsyncSession) -> Note | None:
    query = select(Note).filter(Note.id == note_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def create_note(body: NoteModel, db: AsyncSession) -> Note:
    # Завантажуємо теги асинхронно
    query = select(Tag).filter(Tag.id.in_(body.tags))
    result = await db.execute(query)
    tags = list(result.scalars().all())
    
    note = Note(title=body.title, description=body.description, tags=tags)
    
    db.add(note)
    await db.commit()
    await db.refresh(note)
    return note

async def remove_note(note_id: int, db: AsyncSession) -> Note | None:
    note = await get_note(note_id, db)
    if note:
        await db.delete(note)
        await db.commit()
    return note

async def update_note(note_id: int, body: NoteUpdate, db: AsyncSession) -> Note | None:
    note = await get_note(note_id, db)
    if note: 
        query = select(Tag).filter(Tag.id.in_(body.tags))
        result = await db.execute(query)
        tags = list(result.scalars().all())
        
        note.title = body.title
        note.description = body.description
        note.done = body.done
        note.tags = tags
        await db.commit()
        await db.refresh(note)
    return note

async def update_status_note(note_id: int, body: NoteStatusUpdate, db: AsyncSession) -> Note | None:
    note = await get_note(note_id, db)
    if note:
        note.done = body.done
        await db.commit()
        await db.refresh(note)
    return note
