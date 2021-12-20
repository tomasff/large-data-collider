from discord import Member, Status
from discord.ext.commands import Cog

from .metric_collector import MetricCollector

from ..models import Event, EventType


def _parse_status(status: Status) -> str:
    if status == 'dnd':
        return 'do_not_disturb'

    return str(status)


class StateCollector(MetricCollector):

    @Cog.listener()
    async def on_member_update(self, before: Member, after: Member):
        if before.status == after.status:
            return

        with self.db_sessions.begin() as sess:
            sess.add(Event(event_type=EventType.STATUS_UPDATE.value, meta={
                "before": _parse_status(before.status),
                "after": _parse_status(after.status)
            }))
