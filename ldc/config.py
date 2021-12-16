import os
from dataclasses import dataclass


@dataclass
class Config:
    discord_token: str
    guild_id: int
    database_url: str

    @staticmethod
    def load_from_env():
        return Config(discord_token=os.getenv('DISCORD_TOKEN'),
                      guild_id=int(os.getenv('GUILD_ID')),
                      database_url=Config.build_database_url(
                          url=os.getenv('DB_URL'),
                          user=os.getenv('DB_USER_DISCORD'),
                          password=os.getenv('DB_PASSWORD_DISCORD'),
                          name=os.getenv('DB_NAME')
                      ))

    @staticmethod
    def build_database_url(url: str, user: str, password: str, name: str) -> str:
        return f'postgresql://{user}:{password}@{url}/{name}'
