from discord.ext import commands
import discord

from pymongo import MongoClient
import time
import asyncio

class _cooldown(commands.Cog):
    """Cooldown Reset Cog"""
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()

    global collection
    global prof
    global inbox
    global logdb
    global ventUserId
    global ventInboxProtection
    cluster = MongoClient("mongodb+srv://Edryu:jaisairam4@cluster0.inbe1.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = cluster["Discord"]
    collection = db["vent"]
    
    prof = db["ventProf"]
    inbox = db['ventInbox']
    logdb = db['ventLog']
    ventUserId = db['ventId']
    ventInboxProtection = db['ventInboxProtection']

    @commands.command()
    async def cool(self, ctx, user, sec:int):
        guild = self.bot.get_guild(943556434644328498)
        
        #If uniqueId is provided or userId is provided
        try:
            member = await commands.MemberConverter().convert(ctx, user)
        except commands.errors.MemberNotFound:
            # Check if user input is a unique ID containing alphabets
            if not any(char.isalpha() for char in user):
                await ctx.send('Invalid input. Please provide a valid member ID or unique ID containing alphabets.')
                return
            data = ventUserId.find_one({'uniqueId': user})
            if not data:
                await ctx.send('Could not find a user with the provided unique ID.')
                return
            member = guild.get_member(int(data['user']))
        
        if collection.find_one({'author_id': member.id}): 
            data = collection.find_one({'author_id': member.id})
            channelid = int(data['channel_id'])
            channel = guild.get_channel(channelid)
            await channel.edit(slowmode_delay=0)

            await asyncio.sleep(sec)
           
            await channel.edit(slowmode_delay=7200)


    # @commands.command()
    # @commands.check(lambda ctx: ctx.author.id in admins)
    # async def clean(self, ctx, year: int, month: int, day: int, cutoffRep: int):
    #     """Kicks inactive members of the server (year, month, day, cutoff rep)"""
    #     cutoff_date = pytz.utc.localize(datetime(year, month, day))
    #     kick_count = 0
    #
    #     async def kick_member(member, reason):
    #         em = discord.Embed(color=discord.Color.red())
    #         em.add_field(name="Reason:", value=f"Inactivity in the server since {cutoff_date.date()}", inline=False)
    #         try:
    #             await member.send("You have been kicked out from the server. If you think it was applied in error or you wish to stay active in the server by helping others and yourself, you can rejoin the server from this link: https://disboard.org/server/943556434644328498", embed=em)
    #             await member.kick(reason=reason)
    #         except:
    #             await member.kick(reason=reason)
    #
    #     for member in ctx.guild.members:
    #         if member.bot:
    #             continue
    #         if not ctx.guild.me.guild_permissions.kick_members:
    #             continue
    #
    #         joined_at = member.joined_at
    #         if joined_at is not None and joined_at.replace(tzinfo=pytz.utc) < cutoff_date:
    #             rep = prof.find_one({"user": member.id})
    #             if rep and rep['reputation'] < cutoffRep:
    #                 await kick_member(member, f"Inactivity in the server since {cutoff_date.date()}")
    #                 await ctx.send(f"`{member.display_name}` has been kicked - due to inactivity")
    #                 kick_count += 1
    #             elif not rep:
    #                 await kick_member(member, f"Inactivity in the server since {cutoff_date.date()} (no reputation record found)")
    #                 await ctx.send(f"`{member.display_name}` has been kicked - due to inactivity (no reputation record found)")
    #                 kick_count += 1
    #
    #     await ctx.send(f"`Total members kicked: {kick_count}`")


async def setup(bot):
    await bot.add_cog(_cooldown(bot)) 
