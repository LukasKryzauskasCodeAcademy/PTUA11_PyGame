from typing import Optional
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class Enemy(Base):
    __tablename__ = "enemy"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]]
    max_hp: Mapped[Optional[int]]
    strength: Mapped[Optional[int]]
    potions: Mapped[Optional[int]]

    # def __repr__(self) -> str:
    #     return f"User(id={self.id!r}, name={self.name!r})"