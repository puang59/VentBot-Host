from discord.ext import commands
import discord
import asyncio
from RoboArt import roboart
from datetime import datetime, timedelta
import pytz

from pymongo import MongoClient
from random import *

import config
import tabulate

admins = config.admins
heads = config.ownerIds


class _utility(commands.Cog):
    """Commands for server moderation"""

    def __init__(self, bot):
        self.bot = bot
        self.conn = None

    # config = configparser.ConfigParser()
    # config.read('_ventV2.0/config.ini')

    async def cog_load(self):
        self.conn = await self.bot.get_db_connection()

    global collection
    global prof
    global inbox
    global logdb
    global ventUserId
    global ventInboxProtection

    cluster = MongoClient(config.mongoURI)
    db = cluster["Discord"]

    collection = db["vent"]
    prof = db["ventProf"]
    inbox = db['ventInbox']
    logdb = db['ventLog']
    ventUserId = db['ventId']
    ventInboxProtection = db['ventInboxProtection']

    @commands.command()
    @commands.check(lambda ctx: ctx.author.id in config.ownerIds)
    async def reveal(self, ctx, uniqueId: str):
        confirmation = await ctx.send("Searching...")
        try:
            if ventUserId.find_one({"uniqueId": str(uniqueId)}):
                data = ventUserId.find_one({"uniqueId": str(uniqueId)})
                await confirmation.delete()
                await ctx.author.send(f"<@{data['user']}> - `{uniqueId}`")
                await ctx.message.add_reaction("\U0001f44d")
            else:
                await confirmation.delete()
                await ctx.message.add_reaction("\U0001f44e")
                await ctx.send("Cannot find the matching user id")
        except:
            await confirmation.delete()
            await ctx.message.add_reaction("\U0001f44e")
            await ctx.send("Cannot find the matching user id")

    @commands.command(description="Removes every instance of a user")
    @commands.check(lambda ctx: ctx.author.id in heads)
    async def hardclean(self, ctx, user):
        """Cleans every initials of a member from each database collection"""
        counter = 0
        try:
            collection.delete_many({'author_id': user})  # all vent
            await ctx.channel.send("Cleaned all previous vent messages ..")
            counter += 1
        except Exception as e:
            await ctx.channel.send(f"Failed to clean vent messages: {e}")

        try:
            prof.delete_many({'user': user})  # reputation log
            await ctx.channel.send("Cleaned all reputation log ... ")
            counter += 1
        except Exception as e:
            await ctx.channel.send(f"Failed to clean reputation log: {e}")

        try:
            logdb.delete_many({'userId': user})  # log delete
            await ctx.channel.send("Cleaned all related log ...")
            counter += 1
        except Exception as e:
            await ctx.channel.send(f"Failed to clean related log: {e}")

        try:
            ventUserId.delete_many({'user': user})
            await ctx.channel.send("Cleaned unique user id ...")
            counter += 1
        except Exception as e:
            await ctx.channel.send(f"Failed to clean unique user id: {e}")

        await ctx.channel.send(f"`SuccessCode: {counter}/4`")

    @commands.command(description="DMs everyone in the server | .textall <message>")
    @commands.check(lambda ctx: ctx.author.id in heads)
    async def textall(self, ctx, *, message):
        """DMs everyone in the server"""
        for user in ctx.guild.members:
            try:
                await user.send(message)
                print(f"Sent {user.name} a DM.")
            except:
                print(f"Couldn't DM {user.name}.")
        print("Sent all the server a DM.")

    @commands.command()
    @commands.check(lambda ctx: ctx.author.id in heads)
    async def text(
        self, ctx, members: commands.Greedy[discord.Member], *, msg):
     """DMs specified members of the server"""
     for member in members:
         # Check if user input is a member ID
         if isinstance(member, discord.Member):
             # Member is already a valid member instance
             target_member = member
         else:
             # Check if user input is a unique ID containing alphabets
             if not any(char.isalpha() for char in member):
                 await ctx.send('Invalid input. Please provide a valid member ID or unique ID containing alphabets.')
                 return
             data = ventUserId.find_one({'uniqueId': member})
             if not data:
                 await ctx.send('Could not find a user with the provided unique ID.')
                 return
             target_member = ctx.guild.get_member(int(data['user']))

         try:
             await target_member.send(msg)
             await ctx.send(f'<:agree:943603027313565757> Message sent to {target_member.mention}')
         except:
             await ctx.send(f"<:disagree:943603027854626816> Message couldn't be sent to {target_member.mention}")

    @commands.command()
    @commands.check(lambda ctx: ctx.author.id in heads)
    async def text(
        self, ctx, members: commands.Greedy[discord.Member], *, msg):
        """DMs specified members of the server"""
        if not members:
            await ctx.send('No members provided.')
            return

        for member in members:
            # Check if user input is a member ID
            guild = self.bot.get_guild(943556434644328498)

            # Check if user input is a member ID
            try:
                target_member = await commands.MemberConverter().convert(ctx, str(member))
            except commands.errors.MemberNotFound:
                # Check if user input is a unique ID containing alphabets
                if not any(char.isalpha() for char in member):
                    print(
                        "Invalid input: member ID or unique ID containing alphabets required")
                    await ctx.send('Invalid input. Please provide a valid member ID or unique ID containing alphabets.')
                    return
                data = ventUserId.find_one({'uniqueId': member})
                if not data:
                    print("User not found with the provided unique ID")
                    await ctx.send('Could not find a user with the provided unique ID.')
                    return
                target_member = guild.get_member(int(data['user']))
            print(target_member.name)
            try:
                print("Sending message...")
                await target_member.send(msg)
                await ctx.send(f'<:agree:943603027313565757> Message sent to {target_member.mention}')
            except Exception as e:
                print("Failed to send message:", str(e))
                await ctx.send(f"<:disagree:943603027854626816> Message couldn't be sent to {target_member.mention}")

    @commands.command(description="Removes a user from the DB to maintain lb search")
    @commands.check(lambda ctx: ctx.author.id in admins)
    async def rem(self, ctx, member):
        """Removes a user from the DB to maintain lb search"""
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
        """Terminates the help thread"""
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
    async def kill(self, ctx):
        """Closes private space"""
        if ctx.channel.category.name == "YOUR PRIVATE SPACE":
            await ctx.send("Deleting the channel in 10 seconds!")
            await asyncio.sleep(10)

            with open("channelLife.txt", "r") as file:
                lines = file.readlines()
            channel_id_to_remove = ctx.channel.id

            new_lines = [
    line for line in lines if not line.startswith(
        str(channel_id_to_remove))]

            with open("channelLife.txt", "w") as file:
                file.writelines(new_lines)

            # user channel
            with open("userChannel.txt", "r") as file:
                lines = file.readlines()
            user_id_to_remove = ctx.author.id

            new_lines = [
    line for line in lines if not line.startswith(
        str(user_id_to_remove))]

            with open("userChannel.txt", "w") as file:
                file.writelines(new_lines)

            await ctx.channel.delete()
        else:
            await ctx.send("You cannot kill this channel!", delete_after=10)

    @commands.command()
    async def bin(self, ctx):
        """Closes the inbox channel - Public command"""
        ventsrv = ["📨 INBOX", "📨 INBOX (2)", "📨 INBOX (3)"]

        if ctx.channel.category.name in ventsrv:
            try:
                topic = ctx.channel.topic

                # if the user is reported
                if "Reporter" in topic or "REPORTED" in topic:
                    await ctx.send('We are still investigating the issue!')
                    return

                topicID = ""
                for i, v in enumerate(topic):
                    if v in "0123456789":
                        topicID += v
                guild = self.bot.get_guild(943556434644328498)
                other_chn = guild.get_channel(int(topicID))

                # Deleting data from DB
                inbox.delete_one({"channel": f"{ctx.channel.name}".upper()})

                await ctx.send("Deleting the channel in 10 seconds!")
                await asyncio.sleep(10)
                await ctx.channel.delete()
                await other_chn.delete()
            except Exception as e:
                guild = self.bot.get_guild(943556434644328498)
                usr = guild.get_member(config.admins[3]);
                await usr.send(f"A inbox channel was forcefully closed!!\n```{e}```")

                await ctx.send(f"An Unexpected error occured:\n```{e}````\n**(forcefully closing the channel in 10 seconds)**")
                channel = self.bot.get_channel(ctx.message.channel.id)
                await asyncio.sleep(10)
                await ctx.message.channel.delete()

    @commands.command()
    @commands.check(lambda ctx: ctx.author.id in admins)
    async def find(self, ctx, code):
        """Looks up for the vent message link when code is provided"""
        try:
            data = collection.find_one({"code": code})
            em = discord.Embed()
            em.add_field(name=data["code"], value=data["msg_link"])
            await ctx.send(embed=em)
        except:
            await ctx.send("<:disagree:943603027854626816> Message cannot be found.")

    @commands.command(description="Deletes a vent message when code is provided")
    # @commands.check(lambda ctx: ctx.author.id in admins)
    async def delete(self, ctx, code):
        """Deletes a vent message when code is provided"""
        data = collection.find_one({"code": code})

        channel = self.bot.get_channel(943556439195152477)
        channel2 = self.bot.get_channel(1014201909118251098)
        channel3 = self.bot.get_channel(1035490966934659093)
        channel4 = self.bot.get_channel(1108828942019858582)
        try:
            try:
                txt = await channel.fetch_message(data["msg_id"])
                await txt.delete()
            except:
                txt = await channel2.fetch_message(data["msg_id"])
                await txt.delete()
        except:
            try:
                txt = await channel3.fetch_message(data["msg_id"])
                await txt.delete()
            except:
                txt = await channel4.fetch_message(data["msg_id"])
                await txt.delete()

        collection.delete_one({"code": code})
        await ctx.send("<:agree:943603027313565757> Deleted")

    @commands.command(name="reset")
    @commands.check(lambda ctx: ctx.author.id in admins)
    @commands.cooldown(4, 300, commands.BucketType.member)
    async def reset(self, ctx, user, *, reason = None):
        """Resets the channel cooldown just incase someone requests to edit their vent message"""
        guild = self.bot.get_guild(943556434644328498)
        data = collection.find_one({"code": code})
        member = guild.get_member(int(data["author_id"]))
        ch = self.bot.get_channel(int(data["channel_id"]))
        # role = discord.utils.get(ctx.guild.roles, name="Blocked")
        # await member.remove_roles(role)
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
        """Looks for the uniqueId of vent author"""
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
        """Deletes a vent message when messageid is provided"""
        if collection.find_one({'msg_id': int(id)}):
            data = collection.find_one({'msg_id': int(id)})
            ventChannleIDs = [
    943556439195152477,
    1014201909118251098,
    1035490966934659093,
     1108828942019858582]
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
            ventChannleIDs = [
    943556439195152477,
    1014201909118251098,
    1035490966934659093,
     1108828942019858582]
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
    async def mute(self, ctx, user, *, reason):
        """Timeouts a specified member"""
        if reason == None:
            reason = "None"
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

    @commands.command()
    @commands.check(lambda ctx: ctx.author.id in admins)
    @commands.cooldown(4, 300, commands.BucketType.member)
    async def ban(self, ctx, user, *, reason=None):
        """Removes the existence of the user specified"""
        if reason == None:
            reason = "None"
        guild = self.bot.get_guild(943556434644328498)

        # Check if user input is a member ID
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

        # Ban the member
        try:
            await member.ban(reason=reason)
            await ctx.send('Banned successfully.')
        except discord.errors.Forbidden:
            await ctx.send('I do not have permission to ban this member.')
        except discord.errors.HTTPException:
            await ctx.send('An error occurred while trying to ban this member.')

    @ban.error
    async def on_ban_error(self, ctx, error: Exception):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'This command is on cooldown. Try again in {error.retry_after:.2f}s')

    @commands.command()
    @commands.check(lambda ctx: ctx.author.id in admins)
    async def cleanDb (self, ctx):
        """Deletes all data from ventInboxProtection DB permanently"""
        ventInboxProtection.delete_many({})
        await ctx.send('Done')


    @commands.command()
    @commands.check(lambda ctx: ctx.author.id in admins)
    async def globalwarn(self, ctx, channel: discord.TextChannel, *, message):
        """Posts a warn message in public vent channels just incase theres a chaos between users"""
        ra = roboart()
        if message == None:
            await ctx.send("Please provide a valid message")
        else:
            em = discord.Embed(
                description=f"{message}",
                color=discord.Colour.red()
            )
            warner = ctx.author.name
            art = ra.robo(f"{str(warner)}")
            em.set_author(name="Moderator", icon_url=art)
            x = await channel.send(embed = em)
            await x.add_reaction('\U00002755')


    @commands.command()
    @commands.check(lambda ctx: ctx.author.id in admins)
    async def clean(self, ctx, year: int, month: int, day: int, cutoffRep: int):
        """Kicks inactive members of the server (year, month, day, cutoff rep)"""
        cutoff_date = pytz.utc.localize(datetime(year, month, day))
        kick_count = 0

        async def kick_member(member, reason):
            try:
                nonlocal kick_count  # Mark 'kick_count' as nonlocal
                em = discord.Embed(color=discord.Color.red())
                em.add_field(name="Reason:", value=f"Inactivity in the server since {cutoff_date.date()}", inline=False)
                try:
                    await member.send("You have been kicked out from the server. If you think it was applied in error or you wish to stay active in the server by helping others and yourself, you can rejoin the server from this link: https://disboard.org/server/943556434644328498", embed=em)
                    await member.kick(reason=reason)
                    kick_count += 1
                except:
                    await member.kick(reason=reason)
            except:
                pass

        async def process_members(member_list):
            for member in member_list:
                if member.bot:
                    continue
                if not ctx.guild.me.guild_permissions.kick_members:
                    continue

                joined_at = member.joined_at
                if joined_at is not None and joined_at.replace(tzinfo=pytz.utc) < cutoff_date:
                    rep = prof.find_one({"user": member.id})
                    if rep and rep['reputation'] < cutoffRep:
                        await kick_member(member, f"Inactivity in the server since {cutoff_date.date()}")
                        await ctx.send(f"`{member.display_name}` has been kicked - due to inactivity")
                    elif not rep:
                        await kick_member(member, f"Inactivity in the server since {cutoff_date.date()} (no reputation record found)")
                        await ctx.send(f"`{member.display_name}` has been kicked - due to inactivity (no reputation record found)")

        # Process members in batches to avoid rate limits
        batch_size = 100
        member_list = ctx.guild.members
        for i in range(0, len(member_list), batch_size):
            await process_members(member_list[i:i+batch_size])

        await ctx.send(f"`Total members kicked: {kick_count}`")

    @clean.error
    async def clean_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("You do not have permission to use this command.")

    @commands.command()
    @commands.is_owner()
    async def dbexec(self, ctx, *, query: str):
        """Executes an SQL query and returns the result in a table form"""
        try:
            result = await self.conn.fetch(query)
        except asyncpg.PostgresError as e:
            await ctx.send(f"Error executing the query: {e}")
            return

        # Get the column names from the record keys
        headers = result[0].keys()

        # Format the result in a table form
        rows = [list(row.values()) for row in result]

        # Paginate the table
        table = tabulate.tabulate(rows[:10], headers, tablefmt="fancy_grid")
        message = f"```{table}```"
        await ctx.send(message)

        for i in range(10, len(rows), 10):
            table = tabulate.tabulate(rows[i:i+10], headers, tablefmt="fancy_grid")
            message = f"```{table}```"
            await ctx.send(message)

async def setup(bot):
    await bot.add_cog(_utility(bot))
