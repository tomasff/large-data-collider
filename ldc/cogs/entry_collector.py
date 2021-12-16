from typing import Union

from discord import Member, Guild, User
from discord.ext.commands import Cog

from .metric_collector import MetricCollector

from ..models import Event, EventType


def _get_meta(member: Union[User, Member]):
    return {
        "bot": member.bot
    }


class EntryCollector(MetricCollector):

    @Cog.listener()
    async def on_member_join(self, member: Member):
        with self.db_sessions.begin() as sess:
            sess.add(Event(event_type=EventType.MEMBER_JOIN.value, meta=_get_meta(member)))

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        with self.db_sessions.begin() as sess:
            sess.add(Event(event_type=EventType.MEMBER_LEAVE.value, meta=_get_meta(member)))

    @Cog.listener()
    async def on_member_ban(self, guild: Guild, user: Union[User, Member]):
        with self.db_sessions.begin() as sess:
            sess.add(Event(event_type=EventType.MEMBER_BANNED.value, meta=_get_meta(user)))

    @Cog.listener()
    async def on_member_unban(self, guild: Guild, user: Union[User, Member]):
        with self.db_sessions.begin() as sess:
            sess.add(Event(event_type=EventType.MEMBER_UNBANNED.value, meta=_get_meta(user)))
