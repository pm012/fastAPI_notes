from typing import List
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Note, Tag
from src.schemas import NoteModel, NoteUpdate, NoteStatusUpdate

async def get_notes(skip: int, limit: int, db: AsyncSession) -> List[Note]:
    query = select(Note).options(selectinload(Note.tags)).offset(skip).limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())

async def get_note(note_id: int, db: AsyncSession) -> Note | None:
    query = select(Note).options(selectinload(Note.tags)).filter(Note.id == note_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def create_note(body: NoteModel, db: AsyncSession) -> Note:
    # 1. Search tags, using their  IDs
    query = select(Tag).filter(Tag.id.in_(body.tags))
    result = await db.execute(query)
    tags = list(result.scalars().all())
    
    # 2. Create nots opbject
    note = Note(
        title=body.title, 
        description=body.description, 
        tags=tags
    )
    
    db.add(note)
    
    # Instead commit() doing flush(). 
    # this will generate ID for the note in the database, but will not reset object state.
    await db.flush()
    
    # Saveing generated ID to separate  Python-variable
    generated_id = note.id
    
    # Now we can safely commit transaction
    await db.commit()
    
    # 3. Performing clean asyncronous request using saved variable
    final_query = select(Note).options(selectinload(Note.tags)).filter(Note.id == generated_id)
    final_result = await db.execute(final_query)
    return final_result.scalar_one()

async def remove_note(note_id: int, db: AsyncSession) -> Note | None:
    note = await get_note(note_id, db)
    if note:
        await db.delete(note)
        await db.commit()
    return note

async def update_note(note_id: int, body: NoteUpdate, db: AsyncSession) -> Note | None:
    # Using options(selectinload) for relationships update
    query = select(Note).options(selectinload(Note.tags)).filter(Note.id == note_id)
    result = await db.execute(query)
    note = result.scalar_one_or_none()
    
    if note: 
        tag_query = select(Tag).filter(Tag.id.in_(body.tags))
        tag_result = await db.execute(tag_query)
        tags = list(tag_result.scalars().all())
        
        note.title = body.title
        note.description = body.description
        note.done = body.done
        note.tags = tags
        await db.commit()
        await db.refresh(note)
    return note

async def update_status_note(note_id: int, body: NoteStatusUpdate, db: AsyncSession) -> Note | None:
    query = select(Note).options(selectinload(Note.tags)).filter(Note.id == note_id)
    result = await db.execute(query)
    note = result.scalar_one_or_none()
    
    if note:
        note.done = body.done
        await db.commit()
        await db.refresh(note)
    return note
