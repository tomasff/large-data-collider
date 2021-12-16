import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from discord import Intents
from discord.ext import commands

from .cogs import ReactionCollector, EntryCollector, MessageCollector, VoiceStateCollector, ChannelCollector, \
    EmojiCollector
from .config import Config

logging.basicConfig(level=logging.INFO)

intents = Intents.default()
intents.members = True
intents.bans = True
intents.messages = True
intents.voice_states = True

ldc = commands.Bot(command_prefix='ldc!', intents=intents)


def main():
    config = Config.load_from_env()
    engine = create_engine(config.database_url, future=True)
    db_sessions = sessionmaker(engine)

    ldc.add_cog(ChannelCollector(ldc, db_sessions, config.guild_id))
    ldc.add_cog(EmojiCollector(ldc, db_sessions, config.guild_id))
    ldc.add_cog(ReactionCollector(ldc, db_sessions))
    ldc.add_cog(EntryCollector(ldc, db_sessions))
    ldc.add_cog(MessageCollector(ldc, db_sessions))
    ldc.add_cog(VoiceStateCollector(ldc, db_sessions))

    ldc.run(config.discord_token)


if __name__ == '__main__':
    main()
