from discord.ext import commands
import discord
import asyncio

from prettytable import PrettyTable

import datetime

admins = [943928873412870154, 409994220309577729, 852797584812670996, 751780778802806784, 698895560442118239, 853421799781302302, 657064257552384044]
heads = [943928873412870154, 852797584812670996, 657064257552384044]

class _inboxScanner(commands.Cog):
    """Inbox Scanner that looks for dead inbox channel and deletes them"""
    def __init__(self, bot):
        self.bot = bot

    global inboxscan
    async def inboxscan(self): 
        guild = self.bot.get_guild(943556434644328498)
        logChannel = self.bot.get_channel(1089639606091259994)
        inboxCateg1 = discord.utils.get(guild.categories, name="📨 INBOX")
        inboxCateg2 = discord.utils.get(guild.categories, name="📨 INBOX (2)")
        inboxCateg3 = discord.utils.get(guild.categories, name="📨 INBOX (3)")

        numchannel = 0
        deadchannel = 0
        deleted = 0

        timeScanned = 0
        
        i = 0 
        while i < 1:
            print("########################################")
            print(' _ _ _  _    _|_ _  _|_ _ _|           ')
            print('_)(_(_|| )  _)|_(_|| |_(-(_|  .  .  .  ')
            print("########################################")

            table1 = PrettyTable(["Channel scanned", "Last message", "Current date", "Inactive for"])
            table1.title = 'INBOX (1)'
            table2 = PrettyTable(["Channel scanned", "Last message", "Current date", "Inactive for"])
            table2.title = 'INBOX (2)'
            table3 = PrettyTable(["Channel scanned", "Last message", "Current date", "Inactive for"])
            table3.title = 'INBOX (3)'

            #INBOX 1
            try: 
                for channel in inboxCateg1.channels: 
                    message = await channel.fetch_message(channel.last_message_id)

                    lmsgdate = message.created_at.date()
                    curdate = datetime.datetime.utcnow().date()

                    delta = curdate-lmsgdate

                    if delta.days > 2: 
                        deadchannel +=1 
                        print(f"Deleted {channel.name} from INBOX 1 - inactive for {delta.days} days")
                        print("---------------------------------------------------------------------------")
                        chn = self.bot.get_channel(channel.id)
                        await chn.delete()
                        deadchannel +=1
                        deleted +=1
                        table1.add_row([f"{channel.name}", f"{lmsgdate}", f"{curdate}", f"{delta.days} days"])
                    else: 
                        table1.add_row([f"{channel.name}", f"{lmsgdate}", f"{curdate}", f"{delta.days} days"])

                    numchannel += 1
            except: pass
            #INBOX 2
            try: 
                for channel in inboxCateg2.channels: 
                    message = await channel.fetch_message(channel.last_message_id)

                    lmsgdate = message.created_at.date()
                    curdate = datetime.datetime.utcnow().date()

                    delta = curdate-lmsgdate

                    if delta.days > 2: 
                        deadchannel +=1 
                        print(f"Deleted {channel.name} from INBOX 2 - inactive for {delta.days} days")
                        print("---------------------------------------------------------------------------")
                        chn = self.bot.get_channel(channel.id)
                        await chn.delete()
                        deadchannel +=1
                        deleted +=1
                        table2.add_row([f"{channel.name}", f"{lmsgdate}", f"{curdate}", f"{delta.days} days"])
                    else: 
                        table2.add_row([f"{channel.name}", f"{lmsgdate}", f"{curdate}", f"{delta.days} days"])

                    numchannel += 1
            except: pass
            #INBOX 3
            try: 
                for channel in inboxCateg3.channels: 
                    message = await channel.fetch_message(channel.last_message_id)

                    lmsgdate = message.created_at.date()
                    curdate = datetime.datetime.utcnow().date()

                    delta = curdate-lmsgdate

                    if delta.days > 2: 
                        deadchannel +=1 
                        print(f"Deleted {channel.name} from INBOX 3 - inactive for {delta.days} days")
                        print("---------------------------------------------------------------------------")
                        chn = self.bot.get_channel(channel.id)
                        await chn.delete()
                        deadchannel +=1
                        deleted +=1
                        table3.add_row([f"{channel.name}", f"{lmsgdate}", f"{curdate}", f"{delta.days} days"])
                    else: 
                        table3.add_row([f"{channel.name}", f"{lmsgdate}", f"{curdate}", f"{delta.days} days"])

                    numchannel += 1
            except: pass

            timeScanned += 1
            print("")
            print("Scanning complete ✔")
            print("########## RESULT ##########")
            print("Total channel scanned: ", numchannel)
            print("Dead channels: ", deadchannel)
            print("Channels deleted: ", deleted)
            print("##### DETAILED RESULT #####")
            print(table1)
            print(table2)
            print(table3)
            print(f"--------------------\nScan counter: {timeScanned} times scanned ")
            
            resultEmbed = discord.Embed(
                description=f"**Inbox scanning complete ✔**\n```#### RESULT ####\nTotal channel scanned: {numchannel}\nDead channels: {deadchannel}\nChannels deleted: {deleted}```\n**Scan counter:** {timeScanned} times scanned"
            )
            await logChannel.send(embed = resultEmbed)
            await asyncio.sleep(7200) # 2 hours

    @commands.Cog.listener()
    async def on_ready(self):
        await inboxscan(self)

    @commands.command()
    @commands.check(lambda ctx: ctx.author.id in admins)
    async def scaninbox(self, ctx):
        """Scans inbox channels manually"""
        guild = self.bot.get_guild(943556434644328498)
        logChannel = self.bot.get_channel(1089639606091259994)
        inboxCateg1 = discord.utils.get(guild.categories, name="📨 INBOX")
        inboxCateg2 = discord.utils.get(guild.categories, name="📨 INBOX (2)")
        inboxCateg3 = discord.utils.get(guild.categories, name="📨 INBOX (3)")

        numchannel = 0
        deadchannel = 0
        deleted = 0

        timeScanned = 0
        
        i = 0 
        while i < 1:
            print("########################################")
            print(' _ _ _  _    _|_ _  _|_ _ _|           ')
            print('_)(_(_|| )  _)|_(_|| |_(-(_|  .  .  .  ')
            print("########################################")

            table1 = PrettyTable(["Channel scanned", "Last message", "Current date", "Inactive for"])
            table1.title = 'INBOX (1)'
            table2 = PrettyTable(["Channel scanned", "Last message", "Current date", "Inactive for"])
            table2.title = 'INBOX (2)'
            table3 = PrettyTable(["Channel scanned", "Last message", "Current date", "Inactive for"])
            table3.title = 'INBOX (3)'

            #INBOX 1
            try: 
                for channel in inboxCateg1.channels: 
                    message = await channel.fetch_message(channel.last_message_id)

                    lmsgdate = message.created_at.date()
                    curdate = datetime.datetime.utcnow().date()

                    delta = curdate-lmsgdate

                    if delta.days > 2: 
                        deadchannel +=1 
                        print(f"Deleted {channel.name} from INBOX 1 - inactive for {delta.days} days")
                        print("---------------------------------------------------------------------------")
                        chn = self.bot.get_channel(channel.id)
                        await chn.delete()
                        deadchannel +=1
                        deleted +=1
                        table1.add_row([f"{channel.name}", f"{lmsgdate}", f"{curdate}", f"{delta.days} days"])
                    else: 
                        table1.add_row([f"{channel.name}", f"{lmsgdate}", f"{curdate}", f"{delta.days} days"])

                    numchannel += 1
            except: pass
            #INBOX 2
            try: 
                for channel in inboxCateg2.channels: 
                    message = await channel.fetch_message(channel.last_message_id)

                    lmsgdate = message.created_at.date()
                    curdate = datetime.datetime.utcnow().date()

                    delta = curdate-lmsgdate

                    if delta.days > 2: 
                        deadchannel +=1 
                        print(f"Deleted {channel.name} from INBOX 2 - inactive for {delta.days} days")
                        print("---------------------------------------------------------------------------")
                        chn = self.bot.get_channel(channel.id)
                        await chn.delete()
                        deadchannel +=1
                        deleted +=1
                        table2.add_row([f"{channel.name}", f"{lmsgdate}", f"{curdate}", f"{delta.days} days"])
                    else: 
                        table2.add_row([f"{channel.name}", f"{lmsgdate}", f"{curdate}", f"{delta.days} days"])

                    numchannel += 1
            except: pass
            #INBOX 3
            try: 
                for channel in inboxCateg3.channels: 
                    message = await channel.fetch_message(channel.last_message_id)

                    lmsgdate = message.created_at.date()
                    curdate = datetime.datetime.utcnow().date()

                    delta = curdate-lmsgdate

                    if delta.days > 2: 
                        deadchannel +=1 
                        print(f"Deleted {channel.name} from INBOX 3 - inactive for {delta.days} days")
                        print("---------------------------------------------------------------------------")
                        chn = self.bot.get_channel(channel.id)
                        await chn.delete()
                        deadchannel +=1
                        deleted +=1
                        table3.add_row([f"{channel.name}", f"{lmsgdate}", f"{curdate}", f"{delta.days} days"])
                    else: 
                        table3.add_row([f"{channel.name}", f"{lmsgdate}", f"{curdate}", f"{delta.days} days"])

                    numchannel += 1
            except: pass

            timeScanned += 1
            print("")
            print("Scanning complete ✔")
            print("########## RESULT ##########")
            print("Total channel scanned: ", numchannel)
            print("Dead channels: ", deadchannel)
            print("Channels deleted: ", deleted)
            print("##### DETAILED RESULT #####")
            print(table1)
            print(table2)
            print(table3)
            print(f"--------------------\nScan counter: {timeScanned} times scanned ")
            
            resultEmbed = discord.Embed(
                description=f"**Inbox scanning complete ✔**\n```#### RESULT ####\nTotal channel scanned: {numchannel}\nDead channels: {deadchannel}\nChannels deleted: {deleted}```\n**Scan counter:** {timeScanned} times scanned"
            )
            await logChannel.send(embed = resultEmbed)
            await asyncio.sleep(7200) # 2 hours

async def setup(bot):
    await bot.add_cog(_inboxScanner(bot))

# import discord
# from discord.ext import commands, tasks
# from prettytable import PrettyTable
# import datetime
# import sqlite3
# import os
#
# admins = [943928873412870154, 409994220309577729, 852797584812670996, 751780778802806784, 698895560442118239, 853421799781302302, 657064257552384044]
# heads = [943928873412870154, 852797584812670996, 657064257552384044]
#
# class _inboxScanner(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
#         self.scan_inbox.start()
#
#     def cog_unload(self):
#         self.scan_inbox.cancel()
#
#     async def delete_channel(self, channel):
#         try:
#             await channel.delete()
#             return True
#         except discord.Forbidden:
#             print(f"Failed to delete {channel.name} from {channel.category.name} - Permission denied")
#         except discord.HTTPException:
#             print(f"Failed to delete {channel.name} from {channel.category.name} - HTTP error")
#         return False
#
#     @tasks.loop(hours=5)
#     async def scan_inbox(self):
#         guild = self.bot.get_guild(943556434644328498)
#         if guild is not None:
#             print(f"Guild found: {guild.name}")
#         else:
#             print("Guild not found")
#         log_channel = self.bot.get_channel(1089639606091259994)
#         inbox_categories = ["📨 INBOX", "📨 INBOX (2)", "📨 INBOX (3)"]
#
#         # Connect to the database
#         database_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database', 'scanner.db'))
#         conn = sqlite3.connect(database_path)
#         cursor = conn.cursor()
#
#         # Create the table if it doesn't exist
#         cursor.execute('''CREATE TABLE IF NOT EXISTS summaryId 
#                           (id INTEGER PRIMARY KEY, link TEXT)''')
#
#         # Retrieve the message ID from the database
#         cursor.execute("SELECT id FROM summaryId")
#         result = cursor.fetchone()
#
#         if result:
#             message_id = result[0]
#             try:
#                 summary_message = await log_channel.fetch_message(message_id)
#                 await summary_message.delete()
#                 print(f"Retrieved and deleted summary message with ID: {message_id}")
#             except discord.NotFound:
#                 print(f"Failed to delete summary message with ID: {message_id} - Message not found")
#
#         num_channels = 0
#         dead_channels = 0
#         deleted_channels = 0
#         time_scanned = 0
#         tables = []
#
#         for category_name in inbox_categories:
#             category = discord.utils.get(guild.categories, name=category_name)
#             if category is None or not category.channels:
#                 continue
#
#             table = PrettyTable(["Channel scanned", "Last message", "Current date", "Inactive for"])
#             table.title = category_name
#
#             for channel in category.channels:
#                 try:
#                     last_message = await channel.fetch_message(channel.last_message_id)
#                     last_message_date = last_message.created_at.date()
#                     current_date = datetime.datetime.utcnow().date()
#                     delta = current_date - last_message_date
#
#                     if delta.days > 2:
#                         dead_channels += 1
#                         print(f"Deleted {channel.name} from {channel.category.name} - inactive for {delta.days} days")
#                         if await self.delete_channel(channel):
#                             deleted_channels += 1
#                             table.add_row([channel.name, str(last_message_date), str(current_date), f"{delta.days} days"])
#                     else:
#                         table.add_row([channel.name, str(last_message_date), str(current_date), f"{delta.days} days"])
#
#                     num_channels += 1
#                 except discord.NotFound:
#                     print(f"Failed to fetch message from {channel.name} in {channel.category.name} - Message not found")
#                 except discord.Forbidden:
#                     print(f"Failed to fetch message from {channel.name} in {channel.category.name} - Permission denied")
#                 except discord.HTTPException:
#                     print(f"Failed to fetch message from {channel.name} in {channel.category.name} - HTTP error")
#
#             if table.rowcount > 0:
#                 tables.append(table)
#
#         print("")
#         print("Scanning complete ✔")
#         print("########## RESULT ##########")
#         print("Total channels scanned:", num_channels)
#         print("Dead channels:", dead_channels)
#         print("Channels deleted:", deleted_channels)
#         print("##### DETAILED RESULT #####")
#         for table in tables:
#             print(table)
#             print("--------------------")
#         print("Scan counter:", time_scanned, "times scanned")
#
#         result_embed = discord.Embed(
#             description=f"**Inbox scanning complete ✔**\n```#### RESULT ####\nTotal channels scanned: {num_channels}\nDead channels: {dead_channels}\nChannels deleted: {deleted_channels}```\n**Scan counter:** {time_scanned} times scanned"
#         )
#         log_message = await log_channel.send(embed=result_embed)
#         cursor.execute("INSERT OR REPLACE INTO summaryId (id, link) VALUES (?, ?)", (log_message.id, log_message.jump_url))
#         conn.commit()
#
#         time_scanned += 1
#
#     @commands.Cog.listener()
#     async def on_ready(self):
#         await self.scan_inbox()
#
#     @commands.command()
#     async def scaninbox(self, ctx):
#         """Scans inbox channels manually"""
#         await self.scan_inbox()
#
# def setup(bot):
#     bot.add_cog(_inboxScanner(bot))
