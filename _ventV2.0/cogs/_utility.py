from discord.ext import commands
import discord
import asyncio

from pymongo import MongoClient
from random import *
# import configparser

class _utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # config = configparser.ConfigParser()
    # config.read('_ventV2.0/config.ini')

    global collection
    global prof
    global inbox
    cluster = MongoClient("mongodb+srv://Edryu:jaisairam4@cluster0.inbe1.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = cluster["Discord"]
    collection = db["vent"]
    
    prof = db["ventProf"]
    inbox = db['ventInbox']
    @commands.command()
    async def textall(self, ctx, *, message):
        for user in ctx.guild.members:
            try:
                await user.send(message)
                print(f"Sent {user.name} a DM.")
            except:
                print(f"Couldn't DM {user.name}.")
        print("Sent all the server a DM.")

    @commands.command()
    async def text(self, ctx, members: commands.Greedy[discord.Member], *, msg): 
        for member in members: 
            try: 
                await member.send(msg)
                await ctx.send(f'<:agree:943603027313565757> Message sent to {member.mention}')
            except: 
                await ctx.send(f'<:disagree:943603027854626816> Message couldnt sent to {member.mention}')

    @commands.command()
    async def rem(self, ctx, member = None):
        if not member == None:
            try: 
                prof.delete_one({"user": int(member)})
                await ctx.send("Person removed from the DB")
            except: 
                await ctx.send("Unexpected Error Occured!")
        else: 
            await ctx.send("Cannot find the person!")


@commands.command()
async def close(self, ctx):
    if ctx.channel.category.name == "MAILS":
        topic = ctx.channel.topic
        guild = self.bot.get_guild(943556434644328498)
        member = guild.get_member(int(topic))
        await ctx.send("Deleting the channel in 10 seconds!")
        await asyncio.sleep(10)
        await ctx.channel.delete()
        embedclose = discord.Embed(
            description="This thread is closed now. Thank you very much!"
        )
        embedclose.set_author(
            name="Issue Resolved", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/Sign-check-icon.png/640px-Sign-check-icon.png")
        await member.send(embed=embedclose)


    @commands.command()
    async def bin(self, ctx):
        ventsrv = ["📨 INBOX", "📨 INBOX (2)", "📨 INBOX (3)"]
        if ctx.channel.category.name in ventsrv:
            topic = ctx.channel.topic
            if "Reporter" in topic or "REPORTED" in topic: 
                await ctx.send('We are still investigating the issue!')
                return
            topicID = ""
            for i, v in enumerate(topic):
                if v in "0123456789":
                    topicID += v
            guild = self.bot.get_guild(943556434644328498)
            other_chn = guild.get_channel(int(topicID))

            #Deleting data from DB 
            inbox.delete_one({"channel":f"{ctx.channel.name}".upper()})

            await ctx.send("Deleting the channel in 10 seconds!")
            await asyncio.sleep(10)
            await ctx.channel.delete()
            await other_chn.delete()

    @commands.command()
    async def find(ctx, code):
        try:
            data = collection.find_one({"code": code})
            em = discord.Embed()
            em.add_field(name=data["code"], value=data["msg_link"])
            await ctx.send(embed=em)
        except:
            await ctx.send("<:disagree:943603027854626816> Message cannot be found.")


    @commands.command()
    async def delete(self, ctx, code):
        data = collection.find_one({"code": code})

        channel = self.bot.get_channel(943556439195152477)
        channel2 = self.bot.get_channel(1014201909118251098)
        try: 
            txt = await channel.fetch_message(data["msg_id"])
            await txt.delete()
        except: 
            txt = await channel2.fetch_message(data["msg_id"])
            await txt.delete()    

        collection.delete_one({"code": code})
        await ctx.send("<:agree:943603027313565757> Deleted")


    @commands.command(aliases=["reset"])
    async def edit(self, ctx, code):
        guild = self.bot.get_guild(943556434644328498)
        data = collection.find_one({"code": code})
        member = guild.get_member(int(data["author_id"]))
        ch = self.bot.get_channel(int(data["channel_id"]))
        #role = discord.utils.get(ctx.guild.roles, name="Blocked")
        #await member.remove_roles(role)
        await ch.set_permissions(member, send_messages=True, view_channel=True)

        # deleting message from vent channel
        channel = self.bot.get_channel(943556439195152477)
        txt = await channel.fetch_message(data["msg_id"])
        await txt.delete()
        collection.delete_one({"code": code})

        await ctx.send("<:agree:943603027313565757> Edit opened successfully")

async def setup(bot):
    await bot.add_cog(_utility(bot))
