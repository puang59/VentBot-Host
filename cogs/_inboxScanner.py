from discord.ext import commands
import discord
import asyncio

from prettytable import PrettyTable

import datetime
  
import config

class _inboxScanner(commands.Cog):
    """Inbox Scanner that looks for dead inbox channel and deletes them"""
    def __init__(self, bot):
        self.bot = bot
        self.bot.msgId = 0

    global inboxscan
    async def inboxscan(self): 
        guild = self.bot.get_guild(943556434644328498)
        logChannel = self.bot.get_channel(1089639606091259994)
        inboxCateg1 = discord.utils.get(guild.categories, name="📨 INBOX")
        inboxCateg2 = discord.utils.get(guild.categories, name="📨 INBOX (2)")
        inboxCateg3 = discord.utils.get(guild.categories, name="📨 INBOX (3)")

        msg_id = 0
        
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

            #deleting previous scan log
            if msg_id:
                msg = await logChannel.fetch_message(msg_id)
                await msg.delete()

            resultEmbed = discord.Embed(
                description=f"**Inbox scanning complete ✔**\n```#### RESULT ####\nTotal channel scanned: {numchannel}\nDead channels: {deadchannel}\nChannels deleted: {deleted}```\n**Scan counter:** {timeScanned} times scanned"
            )
            x = await logChannel.send(embed = resultEmbed)
            msg_id = x.id
            await asyncio.sleep(7200) # 2 hours

    @commands.Cog.listener()
    async def on_ready(self):
        await inboxscan(self)

    @commands.command()
    @commands.check(lambda ctx: ctx.author.id in config.admins)
    async def scaninbox(self, ctx):
        """Scans inbox channels manually"""
        guild = self.bot.get_guild(943556434644328498)
        logChannel = self.bot.get_channel(1089639606091259994)
        inboxCateg1 = discord.utils.get(guild.categories, name="📨 INBOX")
        inboxCateg2 = discord.utils.get(guild.categories, name="📨 INBOX (2)")
        inboxCateg3 = discord.utils.get(guild.categories, name="📨 INBOX (3)")

        # Deleting previous scan log
        if self.bot.msgId:
           msg = await logChannel.fetch_message(self.bot.msgId)
           await msg.delete()

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
            resultEmbed.color = 0x2e3137 
            x = await logChannel.send(embed = resultEmbed)
            self.bot.msgId= x.id
            await asyncio.sleep(7200) # 2 hours

async def setup(bot):
    await bot.add_cog(_inboxScanner(bot))
