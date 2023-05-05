from discord.ext import commands
import discord
import asyncio

from datetime import datetime, timedelta

from pymongo import MongoClient
from random import *
# import configparser

admins = [943928873412870154, 409994220309577729, 852797584812670996, 751780778802806784, 698895560442118239, 853421799781302302]
heads = [943928873412870154, 852797584812670996]

class _utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # config = configparser.ConfigParser()
    # config.read('_ventV2.0/config.ini')

    global collection
    global prof
    global inbox
    global logdb
    global ventUserId
    cluster = MongoClient("mongodb+srv://Edryu:jaisairam4@cluster0.inbe1.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = cluster["Discord"]
    collection = db["vent"]
    
    prof = db["ventProf"]
    inbox = db['ventInbox']
    logdb = db['ventLog']
    ventUserId = db['ventId']

    @commands.command(description = "DMs everyone in the server | .textall <message>")
    @commands.check(lambda ctx: ctx.author.id in heads)
    async def textall(self, ctx, *, message):
        for user in ctx.guild.members:
            try:
                await user.send(message)
                print(f"Sent {user.name} a DM.")
            except:
                print(f"Couldn't DM {user.name}.")
        print("Sent all the server a DM.")

    @commands.command()
    @commands.check(lambda ctx: ctx.author.id in heads)
    async def text(self, ctx, members: commands.Greedy[discord.Member], *, msg): 
        characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

        guild = self.bot.get_guild(943556434644328498)
        for member in members: 
            for char in member:
                if char in characters:
                    try: 
                        data = ventUserId.find_one({'uniqueId': str(member)})
                        mem = guild.get_member(int(data['user']))
                        await mem.send(msg)
                        await ctx.send(f'<:agree:943603027313565757> Message sent to {member.mention}')
                        break
                    except Exception as err:
                        await ctx.send(err)
                else: 
                    try: 
                        mem = guild.get_member(int(member))
                        await mem.send(msg)
                        await ctx.send(f'<:agree:943603027313565757> Message sent to {member.mention}')
                        break 
                    except Exception as err:
                        await ctx.send(err)
        '''                
        for member in members: 
            try: 
                await member.send(msg)
                await ctx.send(f'<:agree:943603027313565757> Message sent to {member.mention}')
            except: 
                await ctx.send(f'<:disagree:943603027854626816> Message couldnt sent to {member.mention}')
        '''

    @commands.command(description="Removes a user from the DB to maintain lb search")
    @commands.check(lambda ctx: ctx.author.id in admins)
    async def rem(self, ctx, member = None):
        if not member == None:
            if logdb.find_one({"userId": int(member)}):                
                try: 
                    prof.delete_one({"user": int(member)})
                    logdb.delete_one({"userId": int(member)})
                    await ctx.send("Person removed from the DB")
                except: 
                    await ctx.send("Unexpected Error Occured!")
            else:
                await ctx.send("Please check the ID")
        else: 
            await ctx.send("Cannot find the person!")


    @commands.command()
    @commands.check(lambda ctx: ctx.author.id in admins)
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
    @commands.check(lambda ctx: ctx.author.id in admins)
    async def find(self, ctx, code):
        try:
            data = collection.find_one({"code": code})
            em = discord.Embed()
            em.add_field(name=data["code"], value=data["msg_link"])
            await ctx.send(embed=em)
        except:
            await ctx.send("<:disagree:943603027854626816> Message cannot be found.")


    @commands.command(description="Deletes a vent message when code is provided")
    @commands.check(lambda ctx: ctx.author.id in admins)
    async def delete(self, ctx, code):
        data = collection.find_one({"code": code})

        channel = self.bot.get_channel(943556439195152477)
        channel2 = self.bot.get_channel(1014201909118251098)
        channel3 = self.bot.get_channel(1035490966934659093)
        try: 
            try: 
                txt = await channel.fetch_message(data["msg_id"])
                await txt.delete()
            except: 
                txt = await channel2.fetch_message(data["msg_id"])
                await txt.delete()    
        except: 
            txt = await channel3.fetch_message(data["msg_id"])
            await txt.delete()   

        collection.delete_one({"code": code})
        await ctx.send("<:agree:943603027313565757> Deleted")


    @commands.command(aliases=["reset"])
    @commands.check(lambda ctx: ctx.author.id in admins)
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
    
    '''Unique user id commands'''

    @commands.command(description="Looks for the uniqueId of vent author")
    @commands.check(lambda ctx: ctx.author.id in admins)
    async def search(self, ctx, id):
        confirmation = await ctx.send("Searching...")
        try:
            if collection.find_one({"msg_id": int(id)}):
                data = collection.find_one({'msg_id': int(id)})
                await confirmation.delete()
                await ctx.send(f"The mentioned vent (`{data['code']}`) belongs to `{data['uniqueId']}`")
            else: 
                await confirmation.delete()
                await ctx.send(f"Failed to find!")
        except: 
            await confirmation.delete()
            await ctx.send('Failed to find!')

    @commands.command(description="Deletes a vent message when messageid is provided")
    @commands.check(lambda ctx: ctx.author.id in admins)
    @commands.cooldown(4, 300, commands.BucketType.member)
    async def yeet(self, ctx, id):   
        if collection.find_one({'msg_id': int(id)}):
            data = collection.find_one({'msg_id': int(id)})
            ventChannleIDs = [943556439195152477, 1014201909118251098, 1035490966934659093]
            for ids in ventChannleIDs:
                try:
                    channel = self.bot.get_channel(ids)
                    txt = await channel.fetch_message(data['msg_id'])
                    await txt.delete()
                    collection.delete_one({'msg_id': int(id)})
                    await ctx.send("Deleted the vent message!")
                except:
                    continue
        else: 
            ventChannleIDs = [943556439195152477, 1014201909118251098, 1035490966934659093]
            for ids in ventChannleIDs:
                try: 
                    channel = self.bot.get_channel(ids)
                    txt = await channel.fetch_message(id)
                    await txt.delete()
                    await ctx.send("Deleted the vent message!")
                except:
                    continue

    @yeet.error
    async def on_yeet_error(self, ctx, error: Exception):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'This command is on cooldown. Try again in {error.retry_after:.2f}s')

    @commands.command(desciption="Timeouts a member")
    @commands.check(lambda ctx: ctx.author.id in admins)
    @commands.cooldown(4, 300, commands.BucketType.member) 
    async def mute(self, ctx, user, *, reason = None):
        if ventUserId.find_one({"uniqueId": str(user)}):
            data = ventUserId.find_one({'uniqueId': str(user)})
            guild = self.bot.get_guild(943556434644328498)
            member = guild.get_member(int(data['user']))
            timeoutTime = timedelta(minutes=60)
            await member.timeout(timeoutTime, reason=reason)
            await ctx.send(f'__{user} timedout for 60 Minutes!__\n`Reason:` {reason}')
            try:
                await member.send(f'__You have been timedout for 60 Minutes!__\n`Reason:` {reason}')
            except:
                pass
        else: 
            await ctx.send('Cannot find the user!')

    @mute.error
    async def on_mute_error(self, ctx, error: Exception):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'This command is on cooldown. Try again in {error.retry_after:.2f}s')

    @commands.command()
    @commands.check(lambda ctx: ctx.author.id in admins)
    @commands.cooldown(4, 300, commands.BucketType.member)
    async def ban(self, ctx, user, *, reason = None):
        characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

        guild = self.bot.get_guild(943556434644328498)
        for char in user:
            if char in characters: 
                try: 
                    data = ventUserId.find_one({'uniqueId': str(user)})
                    member = guild.get_member(int(data['user']))
                    await member.ban(reason=reason)
                    await ctx.send("Banned successfully!")  
                    break
                except Exception as err:
                    await ctx.send(err)   
            else:
                try: 
                    member = guild.get_member(int(user))
                    await member.ban(reason=reason)
                    await ctx.send('Banned successfully')
                except Exception as err: 
                    await ctx.send(err)
    
    @ban.error
    async def on_ban_error(self, ctx, error: Exception):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'This command is on cooldown. Try again in {error.retry_after:.2f}s')

async def setup(bot):
    await bot.add_cog(_utility(bot))
