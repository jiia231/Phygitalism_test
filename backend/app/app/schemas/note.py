from typing import Optional

from pydantic import BaseModel


# Shared properties
class NoteBase(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None


# Properties to receive on note creation
class NoteCreate(NoteBase):
    title: str


# Properties to receive on note update
class NoteUpdate(NoteBase):
    pass


# Properties shared by models stored in DB
class NoteInDBBase(NoteBase):
    id: int
    title: str
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Note(NoteInDBBase):
    pass


# Properties properties stored in DB
class NoteInDB(NoteInDBBase):
    pass
