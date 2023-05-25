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
    async def reset(self, ctx, user, sec:int):
        """Resets the channel cooldown for specified duration | time should always be in seconds without any character attacked to it like sec, s etc"""
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
            await ctx.send(f"Removed the cooldown for the user `{user}` for: `{sec} seconds`")
            await asyncio.sleep(sec)
           
            await channel.edit(slowmode_delay=7200)
            await ctx.send(f"Cooldown for the user `{user}` is added back.")

async def setup(bot):
    await bot.add_cog(_cooldown(bot)) 
