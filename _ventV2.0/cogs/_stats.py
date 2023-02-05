from discord.ext import commands
import discord

import time

class _stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_bot_uptime(self, *, brief: bool = False) -> str:
        return time.human_timedelta(self.bot.uptime, accuracy=None, brief=brief, suffix=False)

    @commands.command()
    async def uptime(self, ctx):
        """Tells you how long the bot has been up for."""
        await ctx.send(f'Uptime: **{self.get_bot_uptime()}**')
        
async def setup(bot):
    await bot.add_cog(_stats(bot))
