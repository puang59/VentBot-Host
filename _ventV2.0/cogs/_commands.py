from discord.ext import commands
import discord
import asyncio

from pymongo import MongoClient
from random import *
import configparser

class _commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    config = configparser.ConfigParser()
    config.read('_ventV2.0/config.ini')

    global collection
    global prof
    global inbox
    cluster = MongoClient(config['MONGO']['MONGO_URI'])
    db = cluster["Discord"]
    collection = db["vent"]
    
    prof = db["ventProf"]
    inbox = db['ventInbox']

    @commands.command(aliases=["rep"])
    async def reputation(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author

        if prof.find_one({"user": member.id}):
            results = prof.find_one({"user": member.id})
            rep = results["reputation"]
            embed = discord.Embed(
                description=f"Server Reputation:```{rep} rep```", colour=discord.Colour.lighter_grey())
            embed.set_author(name=member.name, icon_url=member.avatar.url)
            await ctx.send(embed=embed)
        else:
            e_txt = await ctx.send("<:disagree:943603027854626816> User not found!")
            await asyncio.sleep(5)
            await e_txt.delete()

    @commands.command()
    async def lb(self, ctx):
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

    @commands.command()
    async def latency(self, ctx): 
        await ctx.send(f'Pong! In `{round(self.bot.latency * 1000)}ms`')

async def setup(bot):
    await bot.add_cog(_commands(bot))
