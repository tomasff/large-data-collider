from discord.ext.commands import Cog, Bot
from sqlalchemy.orm import sessionmaker


class MetricCollector(Cog):
    def __init__(self, bot: Bot, db_sessions: sessionmaker):
        self.bot = bot
        self.db_sessions = db_sessions
