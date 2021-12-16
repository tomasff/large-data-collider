from .base import Base

from dataclasses import dataclass

from sqlalchemy import Column, BigInteger, String
from sqlalchemy.dialects.postgresql import ENUM

from enum import Enum, auto


class ChannelType(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    STAGE = auto()
    VOICE = auto()
    TEXT = auto()


@dataclass
class Channel(Base):
    id: int
    name: str
    channel_type: str

    __tablename__ = 'channels'

    id = Column(BigInteger, primary_key=True, unique=True)
    name = Column(String(100), nullable=False)

    channel_types = tuple(name for name, _ in ChannelType.__members__.items())

    channel_type = Column(ENUM(*channel_types, name='type'), nullable=False)
