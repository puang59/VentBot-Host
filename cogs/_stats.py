from discord.ext import commands
import discord
import time

from .utils import timeFile, formats

import pkg_resources
import datetime

import config

import pygit2
import itertools

class _stats(commands.Cog):
    """Bot statistics"""
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()

    def bot_uptime(self):
        current_time = time.time()
        difference = int(round(current_time - self.bot.start_time))
        minutes, seconds = divmod(difference, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        formatted_uptime = f"{days}d, {hours}h, {minutes}m, {seconds}s"
        return formatted_uptime

    def format_commit(self, commit: pygit2.Commit) -> str:
        short, _, _ = commit.message.partition('\n')
        short_sha2 = commit.hex[0:6]
        commit_tz = datetime.timezone(datetime.timedelta(minutes=commit.commit_time_offset))
        commit_time = datetime.datetime.fromtimestamp(commit.commit_time).astimezone(commit_tz)

        # [`hash`](url) message (offset)
        offset = timeFile.format_relative(commit_time.astimezone(datetime.timezone.utc))
        return f'[`{short_sha2}`](https://github.com/puang59/VentBot-Host/commit/{commit.hex}) {short} ({offset})'

    def get_last_commits(self, count=3):
        repo = pygit2.Repository('.git')
        commits = list(itertools.islice(repo.walk(repo.head.target, pygit2.GIT_SORT_TOPOLOGICAL), count))
        return '\n'.join(self.format_commit(c) for c in commits)

    @commands.command(aliases=["commit", "git", "changes"])
    async def commits(self, ctx, count=3):
        """Shows commit History"""

        revision = self.get_last_commits(count)
        embed = discord.Embed(description='Commit History:\n' + revision)
        embed.set_author(name="GitHub", icon_url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
        embed.timestamp = discord.utils.utcnow()
        await ctx.send(embed=embed)

    @commands.command()
    async def about(self, ctx):
        """Tells you information about the bot itself."""

        revision = self.get_last_commits()
        embed = discord.Embed(description='Latest Changes:\n' + revision)
        embed.title = 'VentBot-Host'
        embed.url = 'https://github.com/puang59/VentBot-Host'
        embed.colour = discord.Colour.blurple()

        ownerId = config.ownerIds
        botOwner = ctx.guild.get_member(ownerId[1])
        embed.set_author(name=str(botOwner.name), icon_url=botOwner.display_avatar.url)

        # statistics
        total_members = 0
        total_unique = len(self.bot.users)

        text = 0
        voice = 0
        guilds = 0
        for guild in self.bot.guilds:
            guilds += 1
            if guild.unavailable:
                continue

            total_members += guild.member_count or 0
            for channel in guild.channels:
                if isinstance(channel, discord.TextChannel):
                    text += 1
                elif isinstance(channel, discord.VoiceChannel):
                    voice += 1

        embed.add_field(name='Members', value=f'{total_members} total\n{total_unique} unique')
        embed.add_field(name='Channels', value=f'{text + voice} total\n{text} text\n{voice} voice')

        version = pkg_resources.get_distribution('discord.py').version
        uptime = self.bot_uptime()
        embed.add_field(name='Uptime', value=uptime)
        embed.set_footer(text=f'Made with discord.py v{version}', icon_url='http://i.imgur.com/5BFecvA.png')
        embed.timestamp = discord.utils.utcnow()
        await ctx.send(embed=embed)

    @commands.command()
    async def uptime(self, ctx):
        """Shows the total uptime of the bot"""
        uptime = self.bot_uptime()
        await ctx.send(f"Uptime: **{uptime}**")

    @commands.command()
    async def latency(self, ctx):
        """Shows the latency of the bot"""
        await ctx.send(f'Pong! In `{round(self.bot.latency * 1000)}ms`')

async def setup(bot):
    await bot.add_cog(_stats(bot))
