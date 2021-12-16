import logging

import unicodedata

from typing import Union

from discord import Reaction, User, Emoji, PartialEmoji
from discord.ext.commands import Cog

from .metric_collector import MetricCollector

from ..models import Event, EventType


def _get_emoji_type(emoji: Union[Emoji, PartialEmoji, str]) -> str:
    if isinstance(emoji, str):
        return "UNICODE"
    else:
        return "CUSTOM"


def _get_emoji_id(emoji: Union[Emoji, PartialEmoji, str]) -> str:
    if isinstance(emoji, str):
        return unicodedata.name(emoji)
    else:
        return emoji.id


def _parse_reaction(reaction: Reaction) -> dict:
    return {
        "channel_id": reaction.message.channel.id,
        "emoji_id": _get_emoji_id(reaction.emoji),
        "emoji_type": _get_emoji_type(reaction.emoji)
    }


class ReactionCollector(MetricCollector):

    @Cog.listener()
    async def on_reaction_add(self, reaction: Reaction, user: User):
        with self.db_sessions.begin() as sess:
            sess.add(Event(event_type=EventType.REACT_ADD.value, meta=_parse_reaction(reaction)))

    @Cog.listener()
    async def on_reaction_remove(self, reaction: Reaction, user: User):
        with self.db_sessions.begin() as sess:
            sess.add(Event(event_type=EventType.REACT_REMOVE.value, meta=_parse_reaction(reaction)))
