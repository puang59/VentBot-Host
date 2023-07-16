from discord.ext import commands
import discord
import asyncio

from pymongo import MongoClient
from random import *

import config

class _commands(commands.Cog):
    """General server commands"""
    def __init__(self, bot):
        self.bot = bot
        self.conn = None
    
    # config = configparser.ConfigParser()
    # config.read('_ventV2.0/config.ini')

    global collection
    global prof
    global inbox
    cluster = MongoClient(config.mongoURI)
    db = cluster["Discord"]

    collection = db["vent"]
    prof = db["ventProf"]
    inbox = db['ventInbox']

    # Getting back the connection from launcher file
    @commands.Cog.listener()
    async def on_ready(self):
        self.conn = await self.bot.get_db_connection()

    @commands.command(aliases=["rep"])
    @commands.check(lambda ctx: ctx.author.id in config.admins)
    async def reputation(self, ctx, member: discord.Member):
        """Shows reputation earned by the specificed user"""
        if member == None:
            member = ctx.author

        query = "SELECT * FROM reputation WHERE userID = $1;"
        data = await self.conn.fetchrow(query, str(member.id))
        if data:
            rep = data['reputation']
            embed = discord.Embed(
                description=f"Server Reputation:```{rep} rep```", colour=discord.Colour.lighter_grey())
            embed.set_author(name=member.name, icon_url=member.avatar.url)
            await ctx.send(embed=embed)
        else:
            insert_query = "INSERT INTO reputation (userID, reputation) VALUES ($1, $2)"
            await self.conn.execute(insert_query, str(member.id), "0")
            await ctx.send("You don't have any server activity as of now.")

    @commands.command()
    @commands.check(lambda ctx: ctx.author.id in config.admins)
    async def lb(self, ctx):
        """Shows reputation leaderboard"""
        results = prof.find({}).sort("reputation", -1)
        temp = ""
        i = 1
        arg = 50
        guild = self.bot.get_guild(943556434644328498)
        for result in results:
            if i == 1:
                member = guild.get_member(result['user'])
                embed_show = "🥇 `" + \
                    "{:,}".format(
                        result["reputation"]) + " rep` - " + f'{member.name}' + "\n"
                temp += embed_show
            elif i == 2:
                member = guild.get_member(result['user'])
                embed_show = "🥈 `" + \
                    "{:,}".format(result["reputation"]) + \
                    " rep` - " + f'{member.name}' + "\n"
                temp += embed_show
            elif i == 3:
                member = guild.get_member(result['user'])
                embed_show = "🥉 `" + \
                    "{:,}".format(result["reputation"]) + \
                    " rep` - " + f'{member.name}' + "\n"
                temp += embed_show
            else:
                member = guild.get_member(result['user'])
                embed_show = "<:blank:988101402314297384>  `" + \
                    "{:,}".format(result["reputation"]) + \
                    " rep` - " + f'{member.name}' + "\n"
                temp += embed_show
                

            # Top 10 users
            if i == arg:
                break
            else:
                i += 1
        if temp:
            embed = discord.Embed(description=f"{temp}", color=0xFFFFFF)
            embed.set_author(name="Reputation Leaderboard",
                                icon_url="https://cdn.discordapp.com/icons/943556434644328498/901cbfed0350db86feaee903637f477b.webp?size=240")
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(_commands(bot))
