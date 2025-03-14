from discord.ext import commands, tasks
import discord
import asyncio
import os
from random import *
from pymongo import MongoClient
import subprocess
from datetime import datetime
import contextlib

from cogs.utils.help_utils import HelpEmbed, MyHelp

import asyncpg
import config

import pygit2
import itertools

import time

cluster = MongoClient(config.mongoURI)
db = cluster["Discord"]
stories = db['webVent']

intents = discord.Intents.all()
intents.members = True
ventText = stories.find_one({"guild": "vent"})

async def create_db_pool():
    return await asyncpg.create_pool(config.postgresURI)

class VentBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_extensions = [
            'cogs._autoRole',
            'cogs._commands',
            'cogs._cooldown',
            'cogs._dmsupport',
            'cogs._errorHandler',
            'cogs._events',
            'cogs._inboxProtection',
            'cogs._inboxScanner',
            'cogs._logger',
            'cogs._stats',
            'cogs._utility',
            'jishaku'
        ]
        self.db_pool = None
        self.db_connection = None

    # Setting up database with table queries
    async def setup_db(self):
        self.db_pool = await create_db_pool()
        self.db_connection = await self.db_pool.acquire()
        # Create tables if not exists
        queries = [
            """
            CREATE TABLE IF NOT EXISTS reputation(
                userID NUMERIC(50, 0) PRIMARY KEY,
                rep NUMERIC(10, 0)
            );
            """,
        ]

        async with self.db_pool.acquire() as connection:
            for query in queries:
                await connection.execute(query)

    global check_if_allowed
    def check_if_allowed(ctx):
        return ctx.author.id in config.admins

    async def setup_hook(self) -> None:
        for ext in self.initial_extensions:
            await self.load_extension(ext)

    async def on_ready(self):
        print(" \\ \\ / / __| \\| |_   _|  ___  / __| |_ __ _ _  _    /_\\  _ _  ___ _ _ _  _ _ __  ___ _  _ ___")
        print("  \\ V /| _|| .` | | |   |___| \\__ \\  _/ _` | || |  / _ \\| ' \\/ _ \\ ' \\ || | '  \\/ _ \\ || (_-<")
        print("   \\_/ |___|_|\\_| |_|         |___/\\__\\__,_|\\_, | /_/ \\_\\_||_\\___/_||_\\_, |_|_|_\\___/\\_,_/__/")
        print("                                            |__/                      |__/                   ")

    async def start(self, *args, **kwargs):
        await self.setup_db()
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

bot = VentBot(
    command_prefix=".",
    intents=intents,
    activity=discord.Activity(type=discord.ActivityType.listening, name=f"{ventText['stories']}+ stories"),
    owner_ids=config.ownerIds
)
help_command = MyHelp(bot)
bot.help_command = help_command
bot.start_time = time.time()

@bot.command()
@commands.check(check_if_allowed)
async def reload(ctx):
    '''Pulls changes from github and reloads cogs'''

    confirmation = await ctx.send("Reloading...")

    repository = pygit2.Repository('.git')
    try:
        subprocess.run(["git", "pull", "origin", "master"])
        cogsList = []
        for ext in bot.initial_extensions:
            await bot.reload_extension(ext)
            cogsList.append(f"[+] {ext}\n")
        await confirmation.delete()
        latest_commit = repository[repository.head.target]
        commit_time = latest_commit.commit_time
        commit_date = datetime.utcfromtimestamp(commit_time).strftime('%d-%m-%Y %H:%M')
        em = discord.Embed(color=0x2e3137)
        em.add_field(name="🔁 Reloaded modules", value=f"```fix\n{''.join(cogsList)}```")
        em.add_field(name="\U0001f6e0 Lastest commit", value=f"```({latest_commit.author.name})``````{latest_commit.hex[0:6]} - {latest_commit.message}``````({commit_date})```")
        await ctx.send(embed=em)

    except commands.ExtensionFailed as e:
        await ctx.send(e)
        await ctx.message.add_reaction('\U0000274e')

bot.run(config.token)
