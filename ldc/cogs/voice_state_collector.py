import logging

from typing import Union

from discord import Member, VoiceState, VoiceChannel, StageChannel
from discord.ext.commands import Cog

from .metric_collector import MetricCollector

from ..models import Event, EventType


def _get_vc_event_type(before: VoiceState, after: VoiceState) -> EventType:
    if not before.channel and after.channel:
        return EventType.VC_JOIN
    else:
        return EventType.VC_LEAVE


def _get_channel_type(channel: Union[VoiceChannel, StageChannel]):
    if isinstance(channel, VoiceChannel):
        return "VOICE"
    else:
        return "STAGE"


class VoiceStateCollector(MetricCollector):

    @Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        joined_voice = not before.channel and after.channel
        left_voice = before.channel and not after.channel

        if not (joined_voice or left_voice):
            return

        with self.db_sessions.begin() as sess:
            channel = after.channel if joined_voice else before.channel
            event_type = _get_vc_event_type(before, after)

            sess.add(Event(event_type=event_type.value, meta={
                "channel_id": channel.id,
                "channel_type": _get_channel_type(channel)
            }))


