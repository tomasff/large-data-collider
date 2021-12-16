from datetime import datetime
from sqlalchemy import Column, Index, text, DateTime, BigInteger, Integer
from sqlalchemy.ext.indexable import index_property
from sqlalchemy.dialects.postgresql import ENUM, JSONB

from .base import Base

from enum import Enum, auto


class EventType(Enum):
    def _generate_next_value_(self, start, count, last_values):
        return self

    MESSAGE_SEND = auto()
    MESSAGE_DELETE = auto()
    MESSAGE_EDIT = auto()
    MEMBER_JOIN = auto()
    MEMBER_LEAVE = auto()
    MEMBER_BANNED = auto()
    MEMBER_UNBANNED = auto()
    VC_JOIN = auto()
    VC_LEAVE = auto()
    REACT_ADD = auto()
    REACT_REMOVE = auto()


event_types = tuple(name for name, _ in EventType.__members__.items())


class Event(Base):
    __tablename__ = 'events'
    __table_args__ = (
        Index('event_channel_id', text('(meta->>\'channel_id\')'), postgresql_using='hash'),
        Index('event_emoji_id', text('(meta->>\'emoji_id\')'), postgresql_using='hash')
    )

    observed_at = Column(DateTime, unique=True, primary_key=True, default=datetime.utcnow)
    event_type = Column(ENUM(*event_types, name='event_type'))
    meta = Column(JSONB)

    channel_id = index_property('meta', 'channel_id')
    emoji_id = index_property('meta', 'emoji_id')
