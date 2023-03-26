from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Note])
async def read_notes(
    db: AsyncSession = Depends(deps.async_get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve notes.
    """
    if crud.user.is_superuser(current_user):
        notes = await crud.note.get_multi(db, skip=skip, limit=limit)
    else:
        notes = await crud.note.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return notes


@router.post("/", response_model=schemas.Note)
async def create_note(
    *,
    db: AsyncSession = Depends(deps.async_get_db),
    note_in: schemas.NoteCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new note.
    """
    note = await crud.note.create_with_owner(
        db=db, obj_in=note_in, owner_id=current_user.id
    )
    return note


@router.get("/{id}", response_model=schemas.Note)
async def read_note(
    *,
    db: AsyncSession = Depends(deps.async_get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get note by ID.
    """
    note = await crud.note.get(db=db, id=id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if not crud.user.is_superuser(current_user) and (note.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return note


@router.put("/{id}", response_model=schemas.Note)
async def update_note(
    *,
    db: AsyncSession = Depends(deps.async_get_db),
    id: int,
    note_in: schemas.NoteUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a note.
    """
    note = await read_note(db=db, id=id, current_user=current_user)
    note = await crud.note.update(db=db, db_obj=note, obj_in=note_in)
    return note


@router.delete("/{id}", response_model=schemas.Note)
async def delete_note(
    *,
    db: AsyncSession = Depends(deps.async_get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a note.
    """
    note = await read_note(db=db, id=id, current_user=current_user)
    note = crud.note.remove(db=db, id=id)
    return note


@router.delete("/", response_model=schemas.Msg)
async def delete_notes(
    *,
    db: AsyncSession = Depends(deps.async_get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Deletes all user notes.
    """
    await crud.note.delete_multi_by_owner(
        db=db,
        owner_id=current_user.id,
    )
    return {"msg": "Notes are successfully deleted"}
