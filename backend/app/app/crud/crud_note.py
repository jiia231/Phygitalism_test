from typing import List

from fastapi.encoders import jsonable_encoder

# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import delete, select

from app.crud.base import CRUDBase
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate


class CRUDNote(CRUDBase[Note, NoteCreate, NoteUpdate]):
    async def create_with_owner(
        self, db: AsyncSession, *, obj_in: NoteCreate, owner_id: int
    ) -> Note:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_multi_by_owner(
        self, db: AsyncSession, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Note]:
        result = await db.execute(
            select(self.model)
            .filter(Note.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def delete_multi_by_owner(self, db: AsyncSession, *, owner_id: int):
        await db.execute(delete(self.model).filter(Note.owner_id == owner_id))


note = CRUDNote(Note)
