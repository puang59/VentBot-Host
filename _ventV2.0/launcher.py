from discord.ext import commands, tasks
import discord
import asyncio
import os
from random import *
from pymongo import MongoClient
import subprocess
import datetime 
import contextlib
# import configparser
# config = configparser.ConfigParser()
# config.read("_ventV2.0/config.ini")

cluster = MongoClient("mongodb+srv://Edryu:jaisairam4@cluster0.inbe1.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["Discord"]
stories = db['webVent']
    
intents = discord.Intents.all()
intents.members = True
ventText = stories.find_one({"guild": "vent"})


class HelpEmbed(discord.Embed):  # Our embed with some preset attributes to avoid setting it multiple times
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
#        self.timestamp = datetime.datetime.utcnow()
        text = "Use help [command] or help [category] for more information | <> is required | [] is optional"
        self.set_footer(text=text)
        self.color = discord.Color.blurple()

class MyHelp(commands.HelpCommand):
    def __init__(self):
        super().__init__(  # create our class with some aliases and cooldown
            command_attrs={
                "help": "The help command for the bot",
                "cooldown": commands.CooldownMapping.from_cooldown(1, 3.0, commands.BucketType.user),
                "aliases": ['commands']
            }
        )

    async def send(self, **kwargs):
        """a shortcut to sending to get_destination"""
        await self.get_destination().send(**kwargs)

    async def send_bot_help(self, mapping):
        """triggers when a `<prefix>help` is called"""
        ctx = self.context
        embed = HelpEmbed(title=f"{ctx.me.display_name} Help")
        embed.set_thumbnail(url=ctx.me.display_avatar)
        usable = 0

        for cog, commands in mapping.items():  # iterating through our mapping of cog: commands
            if filtered_commands := await self.filter_commands(commands):
                # if no commands are usable in this category, we don't want to display it
                amount_commands = len(filtered_commands)
                usable += amount_commands
                if cog:  # getting attributes dependent on if a cog exists or not
                    name = cog.qualified_name
                    description = cog.description or "No description"
                else:
                    name = "No"
                    description = "Commands with no category"

                embed.add_field(name=f"{name} Category [{amount_commands}]", value=description, inline=False)

        embed.description = f"{len(bot.commands)} commands | {usable} usable"

        await self.send(embed=embed)

    async def send_command_help(self, command):
        """triggers when a `<prefix>help <command>` is called"""
        signature = self.get_command_signature(
            command)  # get_command_signature gets the signature of a command in <required> [optional]
        embed = HelpEmbed(title=signature, description=command.help or "No help found...")

        if cog := command.cog:
            embed.add_field(name="Category", value=cog.qualified_name, inline=False)

        can_run = "No"
        # command.can_run to test if the cog is usable
        with contextlib.suppress(commands.CommandError):
            if await command.can_run(self.context):
                can_run = "Yes"

        embed.add_field(name="Usable", value=can_run, inline=False)

        if command._buckets and (
        cooldown := command._buckets._cooldown):  # use of internals to get the cooldown of the command
            embed.add_field(
                name="Cooldown",
                value=f"{cooldown.rate} per {cooldown.per:.0f} seconds", inline=False,
            )

        await self.send(embed=embed)

    async def send_help_embed(self, title, description, commands):  # a helper function to add commands to an embed
        embed = HelpEmbed(title=title, description=description or "No help found...")

        if filtered_commands := await self.filter_commands(commands):
            for command in filtered_commands:
                embed.add_field(name=self.get_command_signature(command), value=command.help or "No help found...", inline=False)

        await self.send(embed=embed)

    async def send_group_help(self, group):
        """triggers when a `<prefix>help <group>` is called"""
        title = self.get_command_signature(group)
        await self.send_help_embed(title, group.help, group.commands)

    async def send_cog_help(self, cog):
        """triggers when a `<prefix>help <cog>` is called"""
        title = cog.qualified_name or "No"
        await self.send_help_embed(f'{title} Category', cog.description, cog.get_commands())

    async def send_error_message(self, error):
        embed = discord.Embed(title="Error", description=f"Please make sure you are using correct command name. If you are searching for category, make sure you put `_` before category name like `.help _utility`.\n```{error}```")
        channel = self.get_destination()
        await channel.send(embed=embed)

        
class VentBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=".", intents=intents, help_command=MyHelp(), activity=discord.Activity(type=discord.ActivityType.listening, name=f"{ventText['stories']}+ stories"), owner_ids=[943928873412870154, 852797584812670996])
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
    '''Pulls changes from github and reloads cogs'''

    confirmation = await ctx.send("Reloading...")
    try:
        subprocess.run(["git", "pull", "origin", "master"])
        cogsList = []
        for ext in bot.initial_extensions:
            await bot.reload_extension(ext)
            cogsList.append(f"[+] {ext}\n")
        await confirmation.delete()
        em = discord.Embed(color=0x2e3137)
        em.add_field(name="🔁 Reloaded modules", value=f"```fix\n{''.join(cogsList)}```")
        await ctx.send(embed=em)

    except commands.ExtensionFailed as e:
        await ctx.send(e)
        await ctx.message.add_reaction('\U0000274e')

bot.run("OTYyNjAzODQ2Njk2MzM3NDA4.GazOQC.P1jXz9ZcqnT6ZAbnpE9NNJVVd5M53K-04VDHTs")
