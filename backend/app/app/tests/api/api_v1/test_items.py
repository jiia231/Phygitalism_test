import pytest

# from fastapi.testclient import TestClient
from httpx import AsyncClient

# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.tests.utils.note import create_random_note

pytestmark = pytest.mark.asyncio


async def test_create_note(
    client: AsyncClient, superuser_token_headers: dict, async_get_db: AsyncSession
) -> None:
    data = {"title": "Foo", "text": "Fighters"}
    response = await client.post(
        f"{settings.API_V1_STR}/notes/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["text"] == data["text"]
    assert "id" in content
    assert "owner_id" in content


async def test_read_note(
    client: AsyncClient, superuser_token_headers: dict, async_get_db: AsyncSession
) -> None:
    note = await create_random_note(async_get_db)
    response = await client.get(
        f"{settings.API_V1_STR}/notes/{note.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == note.title
    assert content["text"] == note.text
    assert content["id"] == note.id
    assert content["owner_id"] == note.owner_id
