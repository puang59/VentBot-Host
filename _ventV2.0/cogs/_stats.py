from discord.ext import commands
import discord

import time

class _stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()

    @commands.command()
    async def uptime(self, ctx):
        current_time = time.time()
        difference = int(round(current_time - self.start_time))
        minutes, seconds = divmod(difference, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        uptime = f"{days}d, {hours}h, {minutes}m, {seconds}s"
        await ctx.send(f"Bot uptime: {uptime}")

async def setup(bot):
    await bot.add_cog(_stats(bot))
