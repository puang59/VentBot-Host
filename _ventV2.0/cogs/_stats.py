from discord.ext import commands
import discord

import time

class _stats(commands.Cog):
    """Bot statistics"""
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()

    @commands.command()
    async def uptime(self, ctx):
        """Shows the total uptime of the bot"""
        current_time = time.time()
        difference = int(round(current_time - self.start_time))
        minutes, seconds = divmod(difference, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        uptime = f"{days}d, {hours}h, {minutes}m, {seconds}s"
        await ctx.send(f"Uptime: **{uptime}**")


    @commands.command()
    async def latency(self, ctx): 
        """Shows the latency of the bot"""
        await ctx.send(f'Pong! In `{round(self.bot.latency * 1000)}ms`')

async def setup(bot):
    await bot.add_cog(_stats(bot))
