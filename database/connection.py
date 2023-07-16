import discord
from discord.ext import commands
import asyncpg

import config

intents = discord.Intents.all()
intents.members = True

async def create_db_pool():
    return await asyncpg.create_pool(config.postgresURI)

class VentBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="?", intents=intents, owner_ids=config.ownerIds)
        self.initial_extensions = [
            'database.cogs._commands'  
        ]
        self.db_pool = None
        self.db_connection = None

    async def setup_db(self):
        self.db_pool = await create_db_pool()
        self.db_connection = await self.db_pool.acquire()

    async def setup_hook(self) -> None:
        for ext in self.initial_extensions:
            await self.load_extension(ext)

    async def on_ready(self):
        print("Connected to Discord!")

    async def start(self, *args, **kwargs):
        await self.setup_db()
        await self.setup_hook()
        await super().start(*args, **kwargs)

    async def close(self):
        await self.db_pool.release(self.db_connection)
        await self.db_pool.close()
        await super().close()

    async def get_db_connection(self):
        return self.db_connection

    async def on_connect(self):
        print("Connected to Discord!")

    async def on_disconnect(self):
        print("Disconnected from Discord!")

    async def on_resumed(self):
        print("Resumed!")

    async def on_error(self, event_method, *args, **kwargs):
        error_message = f"Error in event {event_method}:"
        error_message += f"\n{args}"
        error_message += f"\n{kwargs}"
        print(error_message)

bot = VentBot()
bot.run(config.token)
