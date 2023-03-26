from typing import Optional

# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models
from app.schemas.note import NoteCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


async def create_random_note(
    db: AsyncSession, *, owner_id: Optional[int] = None
) -> models.Note:
    if owner_id is None:
        user = await create_random_user(db)
        owner_id = user.id
    title = random_lower_string()
    text = random_lower_string()
    note_in = NoteCreate(title=title, text=text, id=id)
    return await crud.note.create_with_owner(db=db, obj_in=note_in, owner_id=owner_id)
