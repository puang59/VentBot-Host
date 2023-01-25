from discord.ext import commands, tasks
import discord
import asyncio
import os
from random import *
from pymongo import MongoClient
import subprocess

import configparser
config = configparser.ConfigParser()
config.read("_ventV2.0/config.ini")

cluster = MongoClient(config["MONGO"]["MONGO_URI"])
db = cluster["Discord"]
stories = db['webVent']
    
intents = discord.Intents.all()
intents.members = True
ventText = stories.find_one({"guild": "vent"})

class VentBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=".", intents=intents, activity=discord.Activity(type=discord.ActivityType.listening, name=f"{ventText['stories']}+ stories"))
        self.initial_extensions = [
            'cogs._commands',
            'cogs._errorHandler',
            'cogs._events',
            'cogs._inboxScanner',
            'cogs._logger',
            'cogs._utility'
        ]

    global check_if_allowed
    def check_if_allowed(ctx):
        admins = [943928873412870154, 409994220309577729, 852797584812670996]
        return ctx.author.id in admins

    async def setup_hook(self) -> None:
        for ext in self.initial_extensions:
            await self.load_extension(ext)

    async def on_ready(self):
        print(" \ \ / / __| \| |_   _|  ___  / __| |_ __ _ _  _    /_\  _ _  ___ _ _ _  _ _ __  ___ _  _ ___")
        print("  \ V /| _|| .` | | |   |___| \__ \  _/ _` | || |  / _ \| ' \/ _ \ ' \ || | '  \/ _ \ || (_-<")
        print("   \_/ |___|_|\_| |_|         |___/\__\__,_|\_, | /_/ \_\_||_\___/_||_\_, |_|_|_\___/\_,_/__/")
        print("                                            |__/                      |__/                   ")

bot = VentBot()

@bot.command()
@commands.check(check_if_allowed)
async def reload(ctx):
    confirmation = await ctx.send("Reloading...")
    try:
        subprocess.run(["git", "pull", "origin", "master"])
        cogsList = []
        for ext in bot.initial_extensions:
            await bot.reload_extension(ext)
            cogsList.append(f"[+] {ext}\n")
        await confirmation.delete()
        em = discord.Embed(color=0x36393f)
        em.add_field(name="🔁 Reloaded modules", value=f"```fix\n{''.join(cogsList)}```")
        await ctx.send(embed=em)

    except commands.ExtensionFailed as e:
        await ctx.send(e)
        await ctx.message.add_reaction('\U0000274e')

bot.run(config["DISCORD"]["TOKEN"])