from discord.ext import commands, tasks
import discord
from discord import CategoryChannel
import asyncio
import os
from random import *

from pymongo import MongoClient

import datetime
import time
from pytz import timezone

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix=".", intents=intents)
bot.remove_command("help")

async def main():
    async with bot:
        print(" \ \ / / __| \| |_   _|  ___  / __| |_ __ _ _  _    /_\  _ _  ___ _ _ _  _ _ __  ___ _  _ ___")
        print("  \ V /| _|| .` | | |   |___| \__ \  _/ _` | || |  / _ \| ' \/ _ \ ' \ || | '  \/ _ \ || (_-<")
        print("   \_/ |___|_|\_| |_|         |___/\__\__,_|\_, | /_/ \_\_||_\___/_||_\_, |_|_|_\___/\_,_/__/")
        print("                                            |__/                      |__/                   ")
        await bot.start('OTYyNjAzODQ2Njk2MzM3NDA4.GazOQC.P1jXz9ZcqnT6ZAbnpE9NNJVVd5M53K-04VDHTs')



@bot.event
async def inboxscan(): 
    guild = bot.get_guild(943556434644328498)
    inboxCateg1 = discord.utils.get(guild.categories, name="📨 INBOX")
    inboxCateg2 = discord.utils.get(guild.categories, name="📨 INBOX (2)")
    inboxCateg3 = discord.utils.get(guild.categories, name="📨 INBOX (3)")

    i = 0 
    while i < 1:
        print("########################################")
        print(' _ _ _  _    _|_ _  _|_ _ _|           ')
        print('_)(_(_|| )  _)|_(_|| |_(-(_|  .  .  .  ')
        print("########################################")

        numchannel = 0
        deadchannel = 0
        deleted = 0
        #INBOX 1
        for channel in inboxCateg1.channels: 
            message = await channel.fetch_message(channel.last_message_id)

            lmsgdate = message.created_at.date()
            curdate = datetime.datetime.utcnow().date()

            delta = curdate-lmsgdate

            if delta.days > 2: 
                deadchannel +=1 
                print(f"Deleted {channel.name} from INBOX 1 - inactive for {delta.days} days")
                print("---------------------------------------------------------------------------")
                chn = bot.get_channel(channel.id)
                await chn.delete()
                deadchannel +=1
                deleted +=1
            else: 
                pass

            numchannel += 1
        #INBOX 2
        for channel in inboxCateg2.channels: 
            message = await channel.fetch_message(channel.last_message_id)

            lmsgdate = message.created_at.date()
            curdate = datetime.datetime.utcnow().date()

            delta = curdate-lmsgdate

            if delta.days > 2: 
                deadchannel +=1 
                print(f"Deleted {channel.name} from INBOX 2 - inactive for {delta.days} days")
                print("---------------------------------------------------------------------------")
                chn = bot.get_channel(channel.id)
                await chn.delete()
                deadchannel +=1
                deleted +=1
            else: 
                pass

            numchannel += 1
        #INBOX 3
        for channel in inboxCateg3.channels: 
            message = await channel.fetch_message(channel.last_message_id)

            lmsgdate = message.created_at.date()
            curdate = datetime.datetime.utcnow().date()

            delta = curdate-lmsgdate

            if delta.days > 2: 
                deadchannel +=1 
                print(f"Deleted {channel.name} from INBOX 3 - inactive for {delta.days} days")
                print("---------------------------------------------------------------------------")
                chn = bot.get_channel(channel.id)
                await chn.delete()
                deadchannel +=1
                deleted +=1
            else: 
                pass

            numchannel += 1

        print("Scanning complete ✔")
        print("########## RESULT ##########")
        print("Total channel scanned: ", numchannel)
        print("Dead channels: ", deadchannel)
        print("Channels deleted: ", deleted)

        await asyncio.sleep(18000) # 5 hours







# @bot.event
# async def diff(): 
#     guild = bot.get_guild(943556434644328498)
#     inboxCateg1 = discord.utils.get(guild.categories, name="📨 INBOX")
#     inboxCateg2 = discord.utils.get(guild.categories, name="📨 INBOX (2)")
#     inboxCateg2 = discord.utils.get(guild.categories, name="📨 INBOX (3)")

#     i = 0 
#     while i < 1:
#         for channel in inboxCateg1.channels: 
#             #print(channel.name)

#             #channel = bot.get_channel(int(943556439195152477))
#             message = await channel.fetch_message(channel.last_message_id)

#             lmsgdate = message.created_at.date()
#             curdate = datetime.datetime.utcnow().date()

#             delta = curdate-lmsgdate

#             if delta.days > 2: 
#                 pass #do something here!!!


#             # lmsgtime = str(message.created_at.time().replace(microsecond=0))
#             # curUTCtime = str(datetime.datetime.utcnow().time().replace(microsecond=0))

#             # l = datetime.datetime.strptime(lmsgtime, "%H:%M:%S")
#             # c = datetime.datetime.strptime(curUTCtime, "%H:%M:%S")

#             # delta = c-l
#             # sec = delta.total_seconds()
#             # hours = sec/(60*60)

#             # print(channel.name)
#             # print("Last message at: ", lmsgtime)
#             # print("Current Time: ", curUTCtime)
#             # print("Difference: ", hours)
#             # print("-----------------------------------------")



#             # print(channel.name)
#             # print("Last message at: ", lmsgdate)
#             # print("Current date: ", curdate)
#             # print("Difference: ", delta.days)
#             # print("-----------------------------------------")

#         await asyncio.sleep(1000)

@bot.event
async def on_ready():
    await inboxscan()

asyncio.run(main())