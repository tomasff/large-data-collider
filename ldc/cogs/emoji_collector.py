import logging

from discord import Emoji
from sqlalchemy.orm import sessionmaker

from discord.ext.commands import Bot, Cog

from .metric_collector import MetricCollector
from ..models import ServerEmoji


def parse_emoji(emoji: Emoji) -> ServerEmoji:
    return ServerEmoji(id=emoji.id, name=emoji.name, url=str(emoji.url))


async def save_or_update_emoji(emoji: Emoji, sess):
    database_emoji = sess.query(ServerEmoji).get(emoji.id)

    if database_emoji:
        logging.info(f'Found existing emoji {emoji.name}.')

        if emoji.name != emoji.name:
            logging.info(f'Detected name update in emoji {emoji.name}.')
            database_emoji.name = emoji.name

        return

    logging.info(f'Found new emoji {emoji.name}.')
    sess.add(parse_emoji(emoji))


class EmojiCollector(MetricCollector):

    def __init__(self,  bot: Bot, db_sessions: sessionmaker, guild_id: int):
        super().__init__(bot, db_sessions)

        self.guild_id = guild_id

    @Cog.listener()
    async def on_ready(self):
        logging.info('Collecting emojis from the target guild')

        guild = self.bot.get_guild(self.guild_id)

        if not guild:
            logging.error('Failed to load the target guild. Cannot collect emojis.')
            return

        with self.db_sessions.begin() as sess:
            for emoji in guild.emojis:
                await save_or_update_emoji(emoji, sess)
