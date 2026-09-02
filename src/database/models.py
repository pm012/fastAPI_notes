from datetime import datetime
from typing import List
from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# 1. Новий спосіб створення базового класу
class Base(DeclarativeBase):
    pass

# 2. Проміжна таблиця для зв'язку "багато до багатьох"
# (Використовує виправлені ForeignKey, про які ми говорили раніше)
note_m2m_tag = Table(
    "note_m2m_tag",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("note_id", Integer, ForeignKey("notes.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE")),
)

class Note(Base):
    __tablename__ = "notes"

    # Mapped[тип] чітко вказує Python, який тип даних тут буде
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(150), nullable=False)
    done: Mapped[bool] = mapped_column(default=False)
    
    # За замовчуванням DateTime підтягує поточний час бази даних через func.now()
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    # Сучасний двосторонній зв'язок (relationship)
    # List["Tag"] вказує, що тут буде список об'єктів Tag
    tags: Mapped[List["Tag"]] = relationship(
        secondary=note_m2m_tag, 
        back_populates="notes"
    )


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25), nullable=False, unique=True)

    # Зворотна сторона зв'язку для Tag
    notes: Mapped[List["Note"]] = relationship(
        secondary=note_m2m_tag, 
        back_populates="tags"
    )
