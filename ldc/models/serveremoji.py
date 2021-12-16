from .base import Base

from dataclasses import dataclass

from sqlalchemy import Column, BigInteger, String


@dataclass
class ServerEmoji(Base):
    id: int
    name: str
    url: str

    __tablename__ = 'emojis'

    id = Column(BigInteger, primary_key=True, unique=True)
    name = Column(String(100), nullable=False)
    url = Column(String(100), nullable=True)
