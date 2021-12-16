import logging

from sqlalchemy.orm import sessionmaker

from discord import ChannelType as GuildChannelType
from discord.abc import GuildChannel
from discord.ext.commands import Bot, Cog

from .metric_collector import MetricCollector
from ..models import Channel, ChannelType


def is_text_or_voice(channel: GuildChannel):
    return channel.type == GuildChannelType.voice or \
           channel.type == GuildChannelType.text


def parse_channel(ch: GuildChannel):
    channel_type = ChannelType.VOICE if ch.type == GuildChannelType.voice else ChannelType.TEXT
    return Channel(id=ch.id, name=ch.name, channel_type=channel_type.value)


async def save_or_update_channel(ch: GuildChannel, sess):
    database_channel = sess.query(Channel).get(ch.id)

    if database_channel:
        logging.info(f'Found existing channel {ch.name} of type {ch.type}.')

        if database_channel.name != ch.name:
            logging.info(f'Detected name update in channel {ch.name}.')
            database_channel.name = ch.name

        return

    logging.info(f'Found new channel {ch.name} of type {ch.type}.')
    sess.add(parse_channel(ch))


class ChannelCollector(MetricCollector):

    def __init__(self,  bot: Bot, db_sessions: sessionmaker, guild_id: int):
        super().__init__(bot, db_sessions)

        self.guild_id = guild_id

    @Cog.listener()
    async def on_ready(self):
        logging.info('Large Data Collider connected to Discord.')
        logging.info('Collecting channel information from the target guild')

        guild = self.bot.get_guild(self.guild_id)

        if not guild:
            logging.error('Failed to load the target guild. Cannot collect channels.')
            return

        with self.db_sessions.begin() as sess:
            for channel in filter(is_text_or_voice, guild.channels):
                await save_or_update_channel(channel, sess)

    @Cog.listener()
    async def on_guild_channel_create(self, ch: GuildChannel):
        if not (ch.type == GuildChannelType.text or ch.type == GuildChannelType.voice):
            return

        with self.db_sessions.begin() as sess:
            await save_or_update_channel(ch, sess)
