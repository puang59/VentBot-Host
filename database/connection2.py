import discord
from discord.ext import commands
import asyncio
import asyncpg

import config

intents = discord.Intents.all()
intents.members = True

async def run():
    description = "A bot written in Python that uses asyncpg to connect to a postgreSQL database."

    # NOTE: 127.0.0.1 is the loopback address. If your db is running on the same machine as the code, this address will work
    credentials = {"user": config.username, "password": config.password, "database": config.database, "host": config.host}
    db = await asyncpg.create_pool(**credentials)

    # Example create table code, you'll probably change it to suit you
    # await db.execute("CREATE TABLE IF NOT EXISTS temp(name VARCHAR(100) NOT NULL, uniqueID VARCHAR(50));")

    bot = Bot(description=description, db=db)
    try:
        await bot.start(config.token)
    except KeyboardInterrupt:
        await db.close()
        await bot.logout()

class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(
            description=kwargs.pop("description"),
            command_prefix="?", 
            intents=intents
        )

        self.db = kwargs.pop("db")

    async def on_ready(self):
        # .format() is for the lazy people who aren't on 3.6+
        print("Username: {0}\nID: {0.id}".format(self.user))

    # Example commands, don't use them
    # Don't even use this format, this is not an example of how to make commands.
    @commands.command()
    async def query(ctx, id):
        query = "SELECT * FROM temp WHERE uniqueid = $1;"

        # This returns a asyncpg.Record object, which is similar to a dict
        row = await bot.db.fetchrow(query, str(id))
        await ctx.send("{}: {}".format(row["name"], row["uniqueid"]))

    @commands.command()
    async def update(ctx, *, new_data: str):
        # Once the code exits the transaction block, changes made in the block are committed to the db

        connection = await bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE users SET data = $1 WHERE id = $2"
            await bot.db.execute(query, new_data, ctx.author.id)
        await bot.db.release(connection)

        await ctx.send("NEW:\n{}: {}".format(ctx.author.id, new_data))

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
