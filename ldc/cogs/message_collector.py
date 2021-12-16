from typing import Union

from discord import Message
from discord.ext.commands import Cog

from .metric_collector import MetricCollector

from ..models import Event, EventType


class MessageCollector(MetricCollector):

    @Cog.listener()
    async def on_message(self, message: Message):
        with self.db_sessions.begin() as sess:
            sess.add(Event(event_type=EventType.MESSAGE_SEND.value, meta={
                "channel_id": message.channel.id
            }))

    @Cog.listener()
    async def on_message_delete(self, message: Message):
        with self.db_sessions.begin() as sess:
            sess.add(Event(event_type=EventType.MESSAGE_DELETE.value, meta={
                "channel_id": message.channel.id
            }))

    @Cog.listener()
    async def on_message_edit(self, before: Message, after: Message):
        with self.db_sessions.begin() as sess:
            sess.add(Event(event_type=EventType.MESSAGE_EDIT.value, meta={
                "channel_id": before.channel.id
            }))
