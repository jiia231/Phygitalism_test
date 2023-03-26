from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User


class Note(Base):
    id: int = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    text = Column(String(500), index=True)
    owner_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    owner: Mapped["User"] = relationship("User", back_populates="notes")
