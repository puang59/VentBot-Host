from discord.ext import commands

class _commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def q(self, ctx, id: str):
        query = "SELECT * FROM temp WHERE uniqueid = $1;"
        db_connection = await self.bot.get_db_connection()
        data = await db_connection.fetchrow(query, id)
        if data:
            name = data['name']
            uniqueid = data['uniqueid']
            await ctx.send(f"Name: {name}\nUniqueID: {uniqueid}")
        else:
            await ctx.send("No data found for the specified ID.")

def setup(bot):
    bot.add_cog(_commands(bot))
