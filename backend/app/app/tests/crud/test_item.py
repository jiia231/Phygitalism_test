import pytest

# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.schemas.note import NoteCreate, NoteUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string

pytestmark = pytest.mark.asyncio


async def test_create_note(async_get_db: AsyncSession) -> None:
    title = random_lower_string()
    text = random_lower_string()
    note_in = NoteCreate(title=title, text=text)
    user = await create_random_user(async_get_db)
    note = await crud.note.create_with_owner(
        db=async_get_db, obj_in=note_in, owner_id=user.id
    )
    assert note.title == title
    assert note.text == text
    assert note.owner_id == user.id


async def test_get_note(async_get_db: AsyncSession) -> None:
    title = random_lower_string()
    text = random_lower_string()
    note_in = NoteCreate(title=title, text=text)
    user = await create_random_user(async_get_db)
    note = await crud.note.create_with_owner(
        db=async_get_db, obj_in=note_in, owner_id=user.id
    )
    stored_note = await crud.note.get(db=async_get_db, id=note.id)
    assert stored_note
    assert note.id == stored_note.id
    assert note.title == stored_note.title
    assert note.text == stored_note.text
    assert note.owner_id == stored_note.owner_id


async def test_update_note(async_get_db: AsyncSession) -> None:
    title = random_lower_string()
    text = random_lower_string()
    note_in = NoteCreate(title=title, text=text)
    user = await create_random_user(async_get_db)
    note = await crud.note.create_with_owner(
        db=async_get_db, obj_in=note_in, owner_id=user.id
    )
    text2 = random_lower_string()
    note_update = NoteUpdate(text=text2)
    note2 = await crud.note.update(db=async_get_db, db_obj=note, obj_in=note_update)
    assert note.id == note2.id
    assert note.title == note2.title
    assert note2.text == text2
    assert note.owner_id == note2.owner_id


async def test_delete_note(async_get_db: AsyncSession) -> None:
    title = random_lower_string()
    text = random_lower_string()
    note_in = NoteCreate(title=title, text=text)
    user = await create_random_user(async_get_db)
    note = await crud.note.create_with_owner(
        db=async_get_db, obj_in=note_in, owner_id=user.id
    )
    note2 = await crud.note.remove(db=async_get_db, id=note.id)
    note3 = await crud.note.get(db=async_get_db, id=note.id)
    assert note3 is None
    assert note2.id == note.id
    assert note2.title == title
    assert note2.text == text
    assert note2.owner_id == user.id
