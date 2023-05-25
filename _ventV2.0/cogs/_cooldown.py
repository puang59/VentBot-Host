from discord.ext import commands
import discord

import time

class _cooldown(commands.Cog):
    """Bot statistics"""
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()

    @commands.command()
    async def cool(self, ctx): 
        await ctx.send('Hello from _cooldown')

async def setup(bot):
    await bot.add_cog(_cooldown(bot))
