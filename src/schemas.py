from datetime import datetime
from typing import List
from pydantic import BaseModel, Field, ConfigDict

class TagModel(BaseModel):
    name: str = Field(max_length=25)
    
class TagResponse(TagModel):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
        
class NoteBase(BaseModel):
    title: str = Field(max_length=50)
    description: str = Field(max_length=150)
    
class NoteModel(NoteBase):
    tags: List[int]
    
class NoteUpdate(NoteModel):
    done: bool
    
class NoteStatusUpdate(BaseModel):
    done: bool
    
class NoteResponse(NoteBase):
    id: int
    done: bool  # Гарантує повернення статусу
    created_at: datetime
    tags: List[TagResponse]
    
    model_config = ConfigDict(from_attributes=True)
