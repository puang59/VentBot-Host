from discord.ext import commands, tasks
import discord
import asyncio
import os
from random import *

from pymongo import MongoClient

import datetime
import time
from pytz import timezone

########## LOGGER #########
import logging, coloredlogs
import logging.handlers

coloredlogs.install()

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='discord.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
# handler.setFormatter(CustomFormatter())
logger.addHandler(handler)

# LOCAL LOGS 
def logInput(type, data): 
    file = open ("ventLog.log", "r")  
    lines = file.readlines()
    file.close()
    if type == "at": 
        curdate = datetime.datetime.now(timezone("Asia/Kolkata"))
        for i in range(len(lines)):
            lines[i] = lines[i].rstrip()
            if "AT" not in lines[i]:
                continue
            else:
                newLine = f"    AT: [{curdate.day}/{curdate.month}/{curdate.year}] - [{time.strftime('%I:%M %p')}]"
                lines[i] = newLine

        with open("ventLog.log", "w") as file:
            for line in lines:
                file.write(line + "\n")

    elif type == "by": 
        for i in range(len(lines)):
            lines[i] = lines[i].rstrip()
            if "BY" not in lines[i]:
                continue
            else:
                newLine = f"    BY: {data}"
                lines[i] = newLine

        with open("ventLog.log", "w") as file:
            for line in lines:
                file.write(line + "\n")

    elif type == "type": 
        for i in range(len(lines)):
            lines[i] = lines[i].rstrip()
            if "TYPE" not in lines[i]:
                continue
            else:
                newLine = f"    TYPE: {data}"
                lines[i] = newLine

        with open("ventLog.log", "w") as file:
            for line in lines:
                file.write(line + "\n")

    elif type == "messageid": 
        for i in range(len(lines)):
            lines[i] = lines[i].rstrip()
            if "MESSAGE_ID" not in lines[i]:
                continue
            else:
                newLine = f"    MESSAGE_ID: {data}"
                lines[i] = newLine

        with open("ventLog.log", "w") as file:
            for line in lines:
                file.write(line + "\n")

############################

intents = discord.Intents.all()
intents.members = True

global cluster
global db
global collection
global prof
cluster = MongoClient(
    "mongodb+srv://Edryu:jaisairam4@cluster0.inbe1.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["Discord"]
collection = db["vent"]
prof = db["ventProf"]
inbox = db['ventInbox']
vCheck = db["ventCheck"]
stories = db['webVent']
vType = db['ventType']
    
ventText = stories.find_one({"guild": "vent"})

bot = commands.Bot(command_prefix=".", intents=intents, activity=discord.Activity(type=discord.ActivityType.listening, name=f"{ventText['stories']}+ stories"))
bot.remove_command("help")

async def pfp():
    pfp = open(f"image.png", "rb").read()

global cofirm
class tagButtons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Neutral",style=discord.ButtonStyle.grey, disabled=False)
    async def neutral_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        data = vCheck.find_one({"user": interaction.user.id})
        vCheck.update_one({"user": interaction.user.id}, {"$set": {"tags": f"{data['tags']}`Neutral`  "}})
        button.disabled=True
        button.label="Neutral"
        await interaction.response.edit_message(view=self)
    # @discord.ui.button(label="Wholesome",style=discord.ButtonStyle.grey, disabled=False)
    # async def wholesome_button(self, interaction:discord.Interaction, button:discord.ui.Button):
    #     data = vCheck.find_one({"user": interaction.user.id})
    #     vCheck.update_one({"user": interaction.user.id}, {"$set": {"tags": f"{data['tags']}`Wholesome`  "}})
    #     button.disabled=True
    #     button.label="Wholesome"
    #     await interaction.response.edit_message(view=self)
    # @discord.ui.button(label="Positive",style=discord.ButtonStyle.grey, disabled=False)
    # async def positive_button(self, interaction:discord.Interaction, button:discord.ui.Button):
    #     data = vCheck.find_one({"user": interaction.user.id})
    #     vCheck.update_one({"user": interaction.user.id}, {"$set": {"tags": f"{data['tags']}`Positive`  "}})
    #     button.disabled=True
    #     button.label="Positive"
    #     await interaction.response.edit_message(view=self)
    @discord.ui.button(label="Negative",style=discord.ButtonStyle.grey, disabled=False)
    async def negative_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        data = vCheck.find_one({"user": interaction.user.id})
        vCheck.update_one({"user": interaction.user.id}, {"$set": {"tags": f"{data['tags']}`Negative`  "}})
        button.disabled=True
        button.label="Negative"
        await interaction.response.edit_message(view=self)
    @discord.ui.button(label="Sexual",style=discord.ButtonStyle.grey, disabled=False)
    async def sexual_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        data = vCheck.find_one({"user": interaction.user.id})
        vCheck.update_one({"user": interaction.user.id}, {"$set": {"tags": f"{data['tags']}`Sexual`  "}})
        button.disabled=True
        button.label="Sexual"
        await interaction.response.edit_message(view=self)
    @discord.ui.button(label="Suicidal",style=discord.ButtonStyle.grey, disabled=False)
    async def suicidal_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        data = vCheck.find_one({"user": interaction.user.id})
        vCheck.update_one({"user": interaction.user.id}, {"$set": {"tags": f"{data['tags']}`Suicidal`  "}})
        button.disabled=True
        button.label="Suicidal"
        await interaction.response.edit_message(view=self)
    @discord.ui.button(label="Gore",style=discord.ButtonStyle.grey, disabled=False)
    async def gore_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        data = vCheck.find_one({"user": interaction.user.id})
        vCheck.update_one({"user": interaction.user.id}, {"$set": {"tags": f"{data['tags']}`Gore`  "}})
        button.disabled=True
        button.label="Gore"
        await interaction.response.edit_message(view=self)
    @discord.ui.button(label="Self-Harm",style=discord.ButtonStyle.grey, disabled=False)
    async def sh_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        data = vCheck.find_one({"user": interaction.user.id})
        vCheck.update_one({"user": interaction.user.id}, {"$set": {"tags": f"{data['tags']}`Self-Harm`  "}})
        button.disabled=True
        button.label="Self-Harm"
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="None",style=discord.ButtonStyle.blurple, disabled=False)
    async def none_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        # data = vCheck.find_one({"user": interaction.user.id})
        vCheck.update_one({"user": interaction.user.id}, {"$set": {"tags": " "}})
        button.disabled=True
        button.label="None" 
        cofirm = await interaction.channel.send("Click on `Envelope` reaction to accept private messages on this vent. (Click on `☘️` if you dont want to accept private message on this vent)\n**Note:** Person who will send private message to you wont be able to know who you are and you wont be able to know who they are.")
        await cofirm.add_reaction("📩")
        await cofirm.add_reaction("☘️")
        await interaction.response.edit_message(view=self)
        await interaction.message.delete()
    @discord.ui.button(label="Done",style=discord.ButtonStyle.green, disabled=False, emoji='👍')
    async def done_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        button.disabled=True
        button.label="Done"
        cofirm = await interaction.channel.send("Click on `Envelope` reaction to accept private messages on this vent. (Click on `☘️` if you dont want to accept private message on this vent)\n**Note:** Person who will send private message to you wont be able to know who you are and you wont be able to know who they are.")
        await cofirm.add_reaction("📩")
        await cofirm.add_reaction("☘️")
        await interaction.response.edit_message(view=self)
        await interaction.message.delete()

class ReportBtn(discord.ui.View):
    def __init__(self, *, timeout=3600):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Report User",style=discord.ButtonStyle.danger, disabled=False)
    async def gray_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        button.disabled=True
        button.label="Reported"
        button.style=discord.ButtonStyle.gray
        await interaction.response.edit_message(view=self)
        channel = bot.get_channel(943909084430729217)
        if inbox.find_one({"reactor":interaction.user.id}):
            data = inbox.find_one({"reactor":interaction.user.id})
            author = bot.get_user(int(data['author']))

            interChn = bot.get_channel(interaction.channel_id)
            txt = await interChn.fetch_message(interaction.message.id)
            em = discord.Embed(description=f"{txt.embeds[0].description}")

            em.set_author(name=f"{author.name} - {data['author']}", icon_url=f"{author.avatar.url}")
            await channel.send(f"{interaction.channel.name} - <#{interaction.channel_id}>", embed=em)
            await interaction.channel.send(content="<:agree:943603027313565757> The user has been reported to the staff team.")
            #blocking the reported user 
            topic = interaction.channel.topic
            chn = interaction.guild.get_channel(int(topic))
            #await chn.set_permissions(author, send_messages=False, view_channel=True)
            await chn.edit(topic=f"{chn.topic}"+" REPORTED")
            await interaction.channel.edit(topic=f"{interaction.channel.topic}"+" Reporter")
            await chn.send("You have been reported by the person your were talking to! We are looking into the matter and will get back to you soon.")
        elif inbox.find_one({"author":interaction.user.id}):
            data = inbox.find_one({"author":interaction.user.id})
            reactor = bot.get_user(int(data['reactor']))

            interChn = bot.get_channel(interaction.channel_id)
            txt = await interChn.fetch_message(interaction.message.id)
            em = discord.Embed(description=f"{txt.embeds[0].description}")

            em.set_author(name=f"{reactor.name} - {data['reactor']}", icon_url=f"{reactor.avatar.url}")
            await channel.send(f"{interaction.channel.name} - <#{interaction.channel_id}>", embed=em)
            await interaction.channel.send(content="<:agree:943603027313565757> The user has been reported to the staff team.")
            #blocking the reported user 
            topic = interaction.channel.topic
            chn = interaction.guild.get_channel(int(topic))
            #await chn.set_permissions(reactor, send_messages=False, view_channel=True)
            await chn.edit(topic=f"{chn.topic}"+" REPORTED")
            await interaction.channel.edit(topic=f"{interaction.channel.topic}"+" Reporter")
            await chn.send("You have been reported by the person your were talking to! We are looking into the matter and will get back to you soon.")
        else: 
            await interaction.channel.send("UhOh! Looks like something went wrong. Please DM me to report the user instead.")

        #print(interaction.channel_id)
        #print(interaction.user.id)

@bot.event
async def status_task():
    while True:
        await bot.change_presence(status=discord.Status.online, activity=discord.Game('Stay strong'))
        await asyncio.sleep(5)
        await bot.change_presence(status=discord.Status.online, activity=discord.Game('DM me for help'))
        await asyncio.sleep(5)


async def load_cogs():
    for filename in os.listdir("./cog"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cog.{filename[:-3]}")

async def main():
    async with bot:
        await load_cogs()
        print(" \ \ / / __| \| |_   _|  ___  / __| |_ __ _ _  _    /_\  _ _  ___ _ _ _  _ _ __  ___ _  _ ___")
        print("  \ V /| _|| .` | | |   |___| \__ \  _/ _` | || |  / _ \| ' \/ _ \ ' \ || | '  \/ _ \ || (_-<")
        print("   \_/ |___|_|\_| |_|         |___/\__\__,_|\_, | /_/ \_\_||_\___/_||_\_, |_|_|_\___/\_,_/__/")
        print("                                            |__/                      |__/                   ")
        await bot.start('OTYyNjAzODQ2Njk2MzM3NDA4.GazOQC.P1jXz9ZcqnT6ZAbnpE9NNJVVd5M53K-04VDHTs')
        

########## INBOX SCANNER ##########

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

@bot.event
async def on_ready():
    await inboxscan()

@bot.event
async def on_member_join(member):
    if member.guild.id == 943556434644328498:
        joinChannel = bot.get_channel(943909084430729217)
        em = discord.Embed(description=f"<:agree:943603027313565757> {member.name} ({member.id}) joined!", colour=discord.Colour.green())
        x = await joinChannel.send(embed=em)  

        try: 
            if not prof.find_one({"user": member.id}):
                post = {"user": member.id, "reputation": 0}
                prof.insert_one(post)

            if member.guild.id == 943556434644328498:
                if collection.find_one({"author_id": member.id}):
                    data = collection.find_one({"author_id": member.id})
                    ch = bot.get_channel(int(data["channel_id"]))
                    await ch.set_permissions(member, send_messages=True, view_channel=True)
                else:
                    try: 
                        guild = member.guild
                        user_a = member
                        role_b = discord.utils.get(member.guild.roles, name="Blocked")

                        categ = discord.utils.get(guild.categories, name="PRIVATE SPACE")
                        #text_channel = await categ.create_text_channel(f"{member.name}s vent")
                        text_channel = await categ.create_text_channel(f"{member.name}s vent {member.discriminator}")
                        await text_channel.set_permissions(user_a, send_messages=True, view_channel=True)
                        await text_channel.set_permissions(guild.default_role, send_messages=False, view_channel=False)
                        await text_channel.set_permissions(role_b, send_messages=False)
                        await text_channel.edit(topic=f"Custom PRIVATE Vent channel for {member.name}")
                        await text_channel.edit(slowmode_delay=7200)

                        ema = discord.Embed(
                            description="1) Make your text fit in one single message because you will be locked out for `2 Hours` after you vent to prevent spams.\n\n2) Dm <@962603846696337408> to get your message deleted or edited (A staff member will assist you).\n\n3) You can DM <@962603846696337408> bot for any help related to the server.\n\nPlease vent here in this channel and not in bot's DM.\n__React with 🔍 emoji for more information__"
                        )
                        ema.set_author(name="Instruction: ",
                                    icon_url="https://cdn.discordapp.com/icons/943556434644328498/901cbfed0350db86feaee903637f477b.webp?size=240")
                        ema.set_footer(
                            text="Note: We dont save your details and message in any separate database.")
                        await text_channel.send(f"Welcome {member.mention}!  (≧◡≦)")
                        a = await text_channel.send(embed=ema)
                        await a.add_reaction('🔍')
                    except: 
                        try: 
                            guild = member.guild
                            user_a = member
                            role_b = discord.utils.get(member.guild.roles, name="Blocked")

                            categ = discord.utils.get(guild.categories, name="PRIVATE SPACE (2)")
                            #text_channel = await categ.create_text_channel(f"{member.name}s vent")
                            text_channel = await categ.create_text_channel(f"{member.name}s vent {member.discriminator}")
                            await text_channel.set_permissions(user_a, send_messages=True, view_channel=True)
                            await text_channel.set_permissions(guild.default_role, send_messages=False, view_channel=False)
                            await text_channel.set_permissions(role_b, send_messages=False)
                            await text_channel.edit(topic=f"Custom PRIVATE Vent channel for {member.name}")
                            await text_channel.edit(slowmode_delay=7200)

                            ema = discord.Embed(
                                description="1) Make your text fit in one single message because you will be locked out for `2 Hours` after you vent to prevent spams.\n\n2) Dm <@962603846696337408> to get your message deleted or edited (A staff member will assist you).\n\n3) You can DM <@962603846696337408> bot for any help related to the server.\n\nPlease vent here in this channel and not in bot's DM.\n__React with 🔍 emoji for more information__"
                            )
                            ema.set_author(name="Instruction: ",
                                        icon_url="https://cdn.discordapp.com/icons/943556434644328498/901cbfed0350db86feaee903637f477b.webp?size=240")
                            ema.set_footer(
                                text="Note: We dont save your details and message in any separate database.")
                            await text_channel.send(f"Welcome {member.mention}!  (≧◡≦)")
                            a = await text_channel.send(embed=ema)
                            await a.add_reaction('🔍')        
                        except: 
                            try: 
                                guild = member.guild
                                user_a = member
                                role_b = discord.utils.get(member.guild.roles, name="Blocked")

                                categ = discord.utils.get(guild.categories, name="PRIVATE SPACE (3)")
                                #text_channel = await categ.create_text_channel(f"{member.name}s vent")
                                text_channel = await categ.create_text_channel(f"{member.name}s vent {member.discriminator}")
                                await text_channel.set_permissions(user_a, send_messages=True, view_channel=True)
                                await text_channel.set_permissions(guild.default_role, send_messages=False, view_channel=False)
                                await text_channel.set_permissions(role_b, send_messages=False)
                                await text_channel.edit(topic=f"Custom PRIVATE Vent channel for {member.name}")
                                await text_channel.edit(slowmode_delay=7200)

                                ema = discord.Embed(
                                    description="1) Make your text fit in one single message because you will be locked out for `2 Hours` after you vent to prevent spams.\n\n2) Dm <@962603846696337408> to get your message deleted or edited (A staff member will assist you).\n\n3) You can DM <@962603846696337408> bot for any help related to the server.\n\nPlease vent here in this channel and not in bot's DM.\n__React with 🔍 emoji for more information__"
                                )
                                ema.set_author(name="Instruction: ",
                                            icon_url="https://cdn.discordapp.com/icons/943556434644328498/901cbfed0350db86feaee903637f477b.webp?size=240")
                                ema.set_footer(
                                    text="Note: We dont save your details and message in any separate database.")
                                await text_channel.send(f"Welcome {member.mention}!  (≧◡≦)")
                                a = await text_channel.send(embed=ema)
                                await a.add_reaction('🔍')   
                            except: 
                                try: 
                                    guild = member.guild
                                    user_a = member
                                    role_b = discord.utils.get(member.guild.roles, name="Blocked")

                                    categ = discord.utils.get(guild.categories, name="PRIVATE SPACE (4)")
                                    #text_channel = await categ.create_text_channel(f"{member.name}s vent")
                                    text_channel = await categ.create_text_channel(f"{member.name}s vent {member.discriminator}")
                                    await text_channel.set_permissions(user_a, send_messages=True, view_channel=True)
                                    await text_channel.set_permissions(guild.default_role, send_messages=False, view_channel=False)
                                    await text_channel.set_permissions(role_b, send_messages=False)
                                    await text_channel.edit(topic=f"Custom PRIVATE Vent channel for {member.name}")
                                    await text_channel.edit(slowmode_delay=7200)

                                    ema = discord.Embed(
                                        description="1) Make your text fit in one single message because you will be locked out for `2 Hours` after you vent to prevent spams.\n\n2) Dm <@962603846696337408> to get your message deleted or edited (A staff member will assist you).\n\n3) You can DM <@962603846696337408> bot for any help related to the server.\n\nPlease vent here in this channel and not in bot's DM.\n__React with 🔍 emoji for more information__"
                                    )
                                    ema.set_author(name="Instruction: ",
                                                icon_url="https://cdn.discordapp.com/icons/943556434644328498/901cbfed0350db86feaee903637f477b.webp?size=240")
                                    ema.set_footer(
                                        text="Note: We dont save your details and message in any separate database.")
                                    await text_channel.send(f"Welcome {member.mention}!  (≧◡≦)")
                                    a = await text_channel.send(embed=ema)
                                    await a.add_reaction('🔍')                                
                                except: 
                                    guild = member.guild
                                    user_a = member
                                    role_b = discord.utils.get(member.guild.roles, name="Blocked")

                                    categ = discord.utils.get(guild.categories, name="PRIVATE SPACE (5)")
                                    #text_channel = await categ.create_text_channel(f"{member.name}s vent")
                                    text_channel = await categ.create_text_channel(f"{member.name}s vent {member.discriminator}")
                                    await text_channel.set_permissions(user_a, send_messages=True, view_channel=True)
                                    await text_channel.set_permissions(guild.default_role, send_messages=False, view_channel=False)
                                    await text_channel.set_permissions(role_b, send_messages=False)
                                    await text_channel.edit(topic=f"Custom PRIVATE Vent channel for {member.name}")
                                    await text_channel.edit(slowmode_delay=7200) 

                                    ema = discord.Embed(
                                        description="1) Make your text fit in one single message because you will be locked out for `2 Hours` after you vent to prevent spams.\n\n2) Dm <@962603846696337408> to get your message deleted or edited (A staff member will assist you).\n\n3) You can DM <@962603846696337408> bot for any help related to the server.\n\nPlease vent here in this channel and not in bot's DM.\n__React with 🔍 emoji for more information__"
                                    )
                                    ema.set_author(name="Instruction: ",
                                                icon_url="https://cdn.discordapp.com/icons/943556434644328498/901cbfed0350db86feaee903637f477b.webp?size=240")
                                    ema.set_footer(
                                        text="Note: We dont save your details and message in any separate database.")
                                    await text_channel.send(f"Welcome {member.mention}!  (≧◡≦)")
                                    a = await text_channel.send(embed=ema)
                                    await a.add_reaction('🔍')                                    
            await x.add_reaction('✔️')
        except:
            await x.add_reaction('❌')

@bot.event
async def on_member_remove(member):
    if member.guild.id == 943556434644328498:
        guild = bot.get_guild(943556434644328498)
        leaveChannel = bot.get_channel(943909084430729217)
        em = discord.Embed(description=f"<:disagree:943603027854626816> {member.name} ({member.id}) left!", colour=discord.Colour.red())
        x = await leaveChannel.send(embed=em)
        try: 
            try:
                try: 
                    memberName = f"{member.name}".lower()
                    modifiedName = ''.join(char for char in memberName if char.isalnum() or char in " ").replace(" ", "-")
                    channel = discord.utils.get(guild.channels, name=f'{modifiedName}s-vent-{member.discriminator}')
                    await channel.delete()
                    collection.delete_many({'author_id': member.id})
                    prof.delete_one({"user": member.id})
                    await x.add_reaction("✔")
                except: 
                    memberName = f"{member.name}".lower()
                    channel = discord.utils.get(guild.channels, name=f'{memberName}s-vent-{member.discriminator}')
                    await channel.delete()
                    collection.delete_many({'author_id': member.id})
                    prof.delete_one({"user": member.id})
                    await x.add_reaction("✔")#h
            except: 
                memberName = f"{member.name}".lower()
                modifiedName = ''.join(char for char in memberName if char.isalnum() or char in " ").replace(" ", "-")
                channel = discord.utils.get(guild.channels, name=f'{modifiedName}s-vent')
                await channel.delete()
                collection.delete_many({'author_id': member.id})
                prof.delete_one({"user": member.id})
                await x.add_reaction("✔")
        except:
            await x.add_reaction('❌')


@bot.event
async def on_user_update(before, after):
    guild = bot.get_guild(943556434644328498)
    if before.name != after.name: 
        try: 
            channel = discord.utils.get(guild.channels, name=f'{before.name}s-vent-{before.discriminator}')
            await channel.edit(name=f'{after.name}s-vent-{after.discriminator}')
        except: 
            channel = discord.utils.get(guild.channels, name=f'{before.name}s-vent')
            await channel.edit(name=f'{after.name}s-vent-{after.discriminator}')

@bot.event
async def on_message(msg):
    if not msg.guild.id == 943556434644328498:
        return 
    if msg.author.guild.id == 943556434644328498:
        if not msg.author.bot:
            if not msg.content.startswith(bot.command_prefix):
                if msg.channel.category.id == 943581279973167155 or msg.channel.category.id == 987993408138248243 or msg.channel.category.id == 987993582701019166 or msg.channel.category.id == 996458874255187978 or msg.channel.category.id == 996459675589554206:
                    if prof.find_one({"user": msg.author.id}):
                        prof.update_one({"user": msg.author.id}, {"$inc": {"reputation": 5}})
                    else: 
                        post = {"user": msg.author.id, "reputation": 5}
                        prof.insert_one(post)
                else: 
                    if prof.find_one({"user": msg.author.id}):
                        prof.update_one({"user": msg.author.id}, {"$inc": {"reputation": 1}})
                    else: 
                        post = {"user": msg.author.id, "reputation": 1}
                        prof.insert_one(post)
            if not msg.author.id == 943928873412870154:
                if msg.channel.id != 943556439195152477:
                    if not isinstance(msg.channel, discord.channel.DMChannel):
                        if not msg.channel.category.id in [950646823654137897, 987983272069976114, 987986457069240401, 943588904622256168]:
                        #if not msg.channel.category.id == 950646823654137897 or not msg.channel.category.id == 987983272069976114 or not msg.channel.category.id == 987986457069240401 or not msg.channel.category.id == 943588904622256168:
                            if not msg.content.startswith(bot.command_prefix): #checking if msg is a commands 
                                if len(msg.clean_content) < 10:
                                    x = await msg.channel.send("<:disagree:943603027854626816> Your message is too small. (Message should have more than 10 characters)")
                                    await asyncio.sleep(10)
                                    await x.delete()
                                else:
                                    characters = '1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
                                    msg_code = "".join(choice(characters)
                                                    for x in range(randint(4, 10)))
                                    #id = "".join(choice(characters)
                                    #                for x in range(randint(4, 10)))

                                    member = msg.author
                                    if msg.author.id == 852797584812670996:
                                        pass
                                    else:
                                        role = discord.utils.get(
                                            msg.guild.roles, name="Blocked")
                                        #await member.add_roles(role)

                                    #vent_channel = bot.get_channel(f"{member.name}s vent")
                                    vent_channel = bot.get_channel(943556439195152477)
                                    casual_channel = bot.get_channel(1014201909118251098)
                                    # if msg.author.id == 852797584812670996:
                                    #     pass
                                    # else:
                                    #     await msg.channel.set_permissions(member, send_messages=False, view_channel=True)
                                    
                                    typeMsg = await msg.channel.send("Click on `🤍` reaction to post your vent in <#943556439195152477> or `🌻` reaction to post your vent in <#1014201909118251098>")
                                    await typeMsg.add_reaction('🤍')
                                    await typeMsg.add_reaction('🌻')

                                    global casual 
                                    async def casual(): 
                                        post = {"author_id": msg.author.id, "msg_id": msg.id, "type": "casual"}
                                        vType.insert_one(post)
                                    
                                    global serious 
                                    async def serious(): 
                                        post = {"author_id": msg.author.id, "msg_id": msg.id, "type": "serious"}
                                        vType.insert_one(post)


                                    global tagEmbedMessage
                                    async def tagEmbedMessage():
                                        vCheck.insert_one({"user": msg.author.id, "tags": "> "})
                                        tagEm = discord.Embed(
                                            description=f"Click on the tags (press 'None' if you want no tag) and when you are done, press 'Done' button\n**Note:** You can select multiple tags."
                                        )
                                        tagEm.set_author(name="Choose Tags", icon_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fcdn1.iconfinder.com%2Fdata%2Ficons%2Fhawcons%2F32%2F698889-icon-146-tag-512.png&f=1&nofb=1")
                                        await msg.channel.send(embed=tagEm, view=tagButtons())
                                    

                                    #print(tagData['tags'])
                                    #em.add_field(name='🏷 Tags', value=tagData['tags'], inline=False)
                                    #em.add_field(name="\u200b", value=msg.content, inline=False)

                                    global cross

                                    async def cross():
                                        tagData = vCheck.find_one({"user": msg.author.id})
                                        ventTypeCheck = vType.find_one({'author_id': msg.author.id})
                                        # check if tag is empty - if yes then remove tags from embed - if no then continue
                                        if ventTypeCheck['type'] == "serious": 
                                            if "Neutral" in tagData['tags'] or "Negative" in tagData['tags'] or "Sexual" in tagData['tags'] or "Suicidal" in tagData['tags'] or "Gore" in tagData['tags'] or "Self-Harm" in tagData['tags']:
                                                em = discord.Embed(
                                                    description=f"{tagData['tags']}\n\n{msg.content}"
                                                )
                                            else: 
                                                em = discord.Embed(
                                                    description=f"{msg.content}"
                                                )
                                        else: 
                                            em = discord.Embed(
                                                description=f"{msg.content}"
                                            )      

                                        em.set_author(name="Anonymous", icon_url="https://res.cloudinary.com/teepublic/image/private/s--UymRXkch--/t_Resized%20Artwork/c_fit,g_north_west,h_1054,w_1054/co_ffffff,e_outline:53/co_ffffff,e_outline:inner_fill:53/co_bbbbbb,e_outline:3:1000/c_mpad,g_center,h_1260,w_1260/b_rgb:eeeeee/c_limit,f_auto,h_630,q_90,w_630/v1570281377/production/designs/6215195_0.jpg")
                                        # Checking vent type
                                        if ventTypeCheck['type'] == "serious": 
                                            x = await vent_channel.send(embed=em)
                                            await x.add_reaction('🫂')
                                        else: 
                                            y = await casual_channel.send(embed=em)
                                            await y.add_reaction('🗣')

                                        logInput('type', f"{ventTypeCheck['type']}")
                                        vType.delete_one({'author_id':msg.author.id})
                                        vCheck.delete_one({'user': msg.author.id})
                                        stories.update_one({"guild": "vent"}, {"$inc": {"stories": 1}})

                                        try: 
                                            post = {"author_id": msg.author.id, "code": f"{msg_code}",
                                                    "msg_link": f"{x.jump_url}", "msg_id": x.id, "channel_id": msg.channel.id, "owner_name": f"{msg.author.name}#{msg.author.discriminator}", "ident": "vent"}
                                            collection.insert_one(post)
                                        except: 
                                            post = {"author_id": msg.author.id, "code": f"{msg_code}",
                                                    "msg_link": f"{y.jump_url}", "msg_id": y.id, "channel_id": msg.channel.id, "owner_name": f"{msg.author.name}#{msg.author.discriminator}", "ident": "vent"}
                                            collection.insert_one(post)

                                        try:
                                            await cofirm.delete()
                                        except:
                                            pass
                                        await msg.reply(f"<:agree:943603027313565757> ||{msg_code}|| - is your message code. __Keep it safe somewhere and dont share.__")
                                        
                                        try:
                                            data = collection.find_one(
                                                {"code": msg_code})
                                            link = data["msg_link"]
                                            emdm = discord.Embed(
                                                description=f"||{msg_code}|| - {link}")
                                            await msg.author.send("<:agree:943603027313565757> Your vent was posted successfully! Heres the vent link with token just incase.", embed=emdm)
                                        except:
                                            print("DMs closed")


                                        ########## LOGGING ##########
                                        logInput('at', "null")
                                        logInput('by', f"{msg.author.name}")
                                        try: 
                                            logInput('messageid', f"{x.id}")
                                        except: 
                                            logInput('messageid', f"{y.id}")

                                    global accept

                                    async def accept():
                                        tagData = vCheck.find_one({"user": msg.author.id})
                                        ventTypeCheck = vType.find_one({'author_id': msg.author.id})
                                        # check if tag is empty - if yes then remove tags from embed - if no then continue
                                        if ventTypeCheck['type'] == "serious": 
                                            if "Neutral" in tagData['tags'] or "Negative" in tagData['tags'] or "Sexual" in tagData['tags'] or "Suicidal" in tagData['tags'] or "Gore" in tagData['tags'] or "Self-Harm" in tagData['tags']:
                                                em = discord.Embed(
                                                    description=f"{tagData['tags']}\n\n{msg.content}"
                                                )
                                            else: 
                                                em = discord.Embed(
                                                    description=f"{msg.content}"
                                                )
                                        else: 
                                            em = discord.Embed(
                                                description=f"{msg.content}"
                                            )

                                        em.set_author(name="Anonymous", icon_url="https://res.cloudinary.com/teepublic/image/private/s--UymRXkch--/t_Resized%20Artwork/c_fit,g_north_west,h_1054,w_1054/co_ffffff,e_outline:53/co_ffffff,e_outline:inner_fill:53/co_bbbbbb,e_outline:3:1000/c_mpad,g_center,h_1260,w_1260/b_rgb:eeeeee/c_limit,f_auto,h_630,q_90,w_630/v1570281377/production/designs/6215195_0.jpg")
                                        em.set_footer(
                                            text="You can click on speech-bubble emoji to reply to this vent and talk to the author anonymously.", icon_url="https://kidsattennis.ca/wp-content/uploads/2020/05/greenball.png")
                                        
                                        # Checking vent type
                                        if ventTypeCheck['type'] == "serious": 
                                            x = await vent_channel.send(embed=em)
                                            await x.add_reaction('🫂')
                                            await x.add_reaction('💬')
                                        else: 
                                            y = await casual_channel.send(embed=em)
                                            await y.add_reaction('🗣')
                                            await y.add_reaction('💬')
                                        logInput('type', f"{ventTypeCheck['type']}")
                                        vType.delete_one({'author_id':msg.author.id})
                                        vCheck.delete_one({'user': msg.author.id})
                                        stories.update_one({"guild": "vent"}, {"$inc": {"stories": 1}})

                                        try: 
                                            post = {"author_id": msg.author.id, "code": f"{msg_code}",
                                                    "msg_link": f"{x.jump_url}", "msg_id": x.id, "channel_id": msg.channel.id, "owner_name": f"{msg.author.name}#{msg.author.discriminator}", "ident": "vent"}
                                            collection.insert_one(post)
                                        except: 
                                            post = {"author_id": msg.author.id, "code": f"{msg_code}",
                                                    "msg_link": f"{y.jump_url}", "msg_id": y.id, "channel_id": msg.channel.id, "owner_name": f"{msg.author.name}#{msg.author.discriminator}", "ident": "vent"}
                                            collection.insert_one(post)
                                        
                                        try:
                                            await cofirm.delete()
                                        except:
                                            pass
                                        await msg.reply(f"<:agree:943603027313565757> ||{msg_code}|| - is your message code. __Keep it safe somewhere and dont share.__")
                                    

                                        try:
                                            data = collection.find_one(
                                                {"code": msg_code})
                                            link = data["msg_link"]
                                            emdm = discord.Embed(
                                                description=f"||{msg_code}|| - {link}")
                                            await msg.author.send("<:agree:943603027313565757> Your vent was posted successfully! Heres the vent link with token just incase.", embed=emdm)
                                        except:
                                            print("DMs closed")

                                        ########## LOGGING ##########
                                        logInput('at', "null")
                                        logInput('by', f"{msg.author.name}")
                                        try: 
                                            logInput('messageid', f"{x.id}")
                                        except: 
                                            logInput('messageid', f"{y.id}")


                # Inbox
                if isinstance(msg.channel, discord.TextChannel):
                    if msg.channel.category is not None:
                        if msg.channel.category.id == 950646823654137897 or msg.channel.category.id == 987983272069976114 or msg.channel.category.id == 987986457069240401: 
                            if not msg.author.bot:
                                if msg.content.startswith("."):
                                    pass
                                else:
                                    if "REPORTED" in msg.channel.topic:
                                        await msg.add_reaction("<:disagree:943603027854626816>")
                                    elif "Reporter" in msg.channel.topic:
                                        print("Reporter channel detected")
                                    else:
                                        topic = msg.channel.topic
                                        
                                        msgContent = msg.content
                                        chn = msg.guild.get_channel(int(topic))
                                        em = discord.Embed(
                                            description=msg.content
                                        )
                                        em.set_author(
                                            name="Stranger", icon_url="https://image.similarpng.com/very-thumbnail/2020/08/Emoji-social-media-Reaction-heart-icon-vector-PNG.png")
                                        x = await chn.send(embed=em, view=ReportBtn())
                                        await msg.add_reaction("<:agree:943603027313565757>")

                await bot.process_commands(msg)

#hm
@bot.command()
async def close(ctx):
    if ctx.channel.category.name == "MAILS":
        topic = ctx.channel.topic
        guild = bot.get_guild(943556434644328498)
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


@bot.command()
async def bin(ctx):
    if ctx.channel.category.name == "📨 INBOX" or ctx.channel.category.name == "📨 INBOX (2)" or ctx.channel.category.name == "📨 INBOX (3)":
        topic = ctx.channel.topic
        if "Reporter" in topic or "REPORTED" in topic: 
            await ctx.send('We are still investigating the issue!')
            return
        topicID = ""
        for i, v in enumerate(topic):
            if v in "0123456789":
                topicID += v
        #print(topicID)
        guild = bot.get_guild(943556434644328498)
        other_chn = guild.get_channel(int(topicID))

        #Deleting data from DB 
        inbox.delete_one({"channel":f"{ctx.channel.name}".upper()})
        # try: 
        #     inbox.delete_one({"reactor": int(ctx.message.author.id)})
        # except: 
        #     inbox.delete_one({"author": int(ctx.message.author.id)})

        await ctx.send("Deleting the channel in 10 seconds!")
        await asyncio.sleep(10)
        await ctx.channel.delete()
        await other_chn.delete()

@bot.command()
async def find(ctx, code):
    try:
        data = collection.find_one({"code": code})
        em = discord.Embed()
        em.add_field(name=data["code"], value=data["msg_link"])
        await ctx.send(embed=em)
    except:
        await ctx.send("<:disagree:943603027854626816> Message cannot be found.")


@bot.command()
async def delete(ctx, code):
    data = collection.find_one({"code": code})

    channel = bot.get_channel(943556439195152477)
    channel2 = bot.get_channel(1014201909118251098)
    try: 
        txt = await channel.fetch_message(data["msg_id"])
        await txt.delete()
    except: 
        txt = await channel2.fetch_message(data["msg_id"])
        await txt.delete()    

    collection.delete_one({"code": code})
    await ctx.send("<:agree:943603027313565757> Deleted")


@bot.command(aliases=["reset"])
async def edit(ctx, code):
    guild = bot.get_guild(943556434644328498)
    data = collection.find_one({"code": code})
    member = guild.get_member(int(data["author_id"]))
    ch = bot.get_channel(int(data["channel_id"]))
    #role = discord.utils.get(ctx.guild.roles, name="Blocked")
    #await member.remove_roles(role)
    await ch.set_permissions(member, send_messages=True, view_channel=True)

    # deleting message from vent channel
    channel = bot.get_channel(943556439195152477)
    txt = await channel.fetch_message(data["msg_id"])
    await txt.delete()
    collection.delete_one({"code": code})

    await ctx.send("<:agree:943603027313565757> Edit opened successfully")

@bot.command()
async def connect(ctx, code): 
    if collection.find_one({"vent_id": code}):
        db_data = collection.find_one({"vent_id": code})
        guild = ctx.author.guild
        user_a = ctx.author
        server = bot.get_guild(943556434644328498)
        msg_owner = server.get_member(int(db_data["author_id"]))

        categ = discord.utils.get(guild.categories, name="📨 INBOX")

        text_channel_replier = await categ.create_text_channel(f"{ctx.author.discriminator}")

        await text_channel_replier.set_permissions(user_a, send_messages=True, view_channel=True)
        await text_channel_replier.set_permissions(msg_owner, view_channel=False)
        await text_channel_replier.set_permissions(guild.default_role, send_messages=False, view_channel=False)
        await text_channel_replier.send(f"You can send your message here and it will be sent to the author automatically! <@{ctx.author.id}>\n__(You can use `.bin` command here to close this inbox)__")

        text_channel_owner = await categ.create_text_channel(f"{ctx.author.discriminator}")

        await text_channel_owner.set_permissions(user_a, view_channel=False)
        await text_channel_owner.set_permissions(msg_owner, send_messages=True, view_channel=True)
        await text_channel_owner.set_permissions(guild.default_role, send_messages=False, view_channel=False)
        await text_channel_owner.edit(topic=f"{str(text_channel_replier.id)}")
        await text_channel_replier.edit(topic=f"{str(text_channel_owner.id)}")
        await text_channel_owner.send(f"Someone wants to talk to you about {db_data['msg_link']}. You'll recieve their message here and you can reply to it by texting here. <@{db_data['author_id']}>\n__(You can use `.bin` command here to close this inbox)__")

        success_embed = discord.Embed(description=f"`Anonymous private message channel:` <#{text_channel_replier.id}>\n\nYou can send message there to chat with vent message author.", colour=discord.Colour.green())
        await ctx.send(embed = success_embed)
    else:
        embed = discord.Embed(description="Cannot find message id in DataBase!", colour=discord.Colour.red())
        await ctx.send(embed = embed)    

@bot.command(pass_context=True)
async def textall(ctx, *, message):
    for user in ctx.guild.members:
        try:
            await user.send(message)
            print(f"Sent {user.name} a DM.")
        except:
            print(f"Couldn't DM {user.name}.")
    print("Sent all the server a DM.")
#h
@bot.command()
async def text(ctx, members: commands.Greedy[discord.Member], *, msg): 
    for member in members: 
        try: 
            await member.send(msg)
            await ctx.send(f'<:agree:943603027313565757> Message sent to {member.mention}')
        except: 
            await ctx.send(f'<:disagree:943603027854626816> Message couldnt sent to {member.mention}')

# @bot.command()
# async def test(ctx, members: commands.Greedy[discord.Member], reason: str):
#     for member in members:
#         await ctx.send(f'{member.mention} {reason}')

@bot.command()
async def rem(ctx, member = None):
    if not member == None:
        try: 
            prof.delete_one({"user": int(member)})
            await ctx.send("Person removed from the DB")
        except: 
            await ctx.send("Unexpected Error Occured!")
    else: 
        await ctx.send("Cannot find the person!")


@bot.command(aliases=["rep"])
async def reputation(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author

    if prof.find_one({"user": member.id}):
        results = prof.find_one({"user": member.id})
        #collection.update_one({"user": member.id}, {"$inc": {"reputation": -int(results["recent"])}})

        #value = random.randint(0, 0xffffff)
        rep = results["reputation"]
        embed = discord.Embed(
            description=f"Server Reputation:```{rep} rep```", colour=discord.Colour.lighter_grey())
        embed.set_author(name=member.name, icon_url=member.avatar.url)
        await ctx.send(embed=embed)
    else:
        e_txt = await ctx.send("<:disagree:943603027854626816> User not found!")
        await asyncio.sleep(5)
        await e_txt.delete()

@bot.command()
async def lb(ctx):
    # <:blank:988101402314297384> 
    results = prof.find({}).sort("reputation", -1)
    temp = ""
    i = 1
    arg = 50
    guild = bot.get_guild(943556434644328498)
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
        #embed.set_thumbnail(
        #    url="https://cdn.discordapp.com/icons/943556434644328498/901cbfed0350db86feaee903637f477b.webp?size=240")
        #embed.add_field(name=result["username"], value=str(result["msg"]))
        embed.set_author(name="Reputation Leaderboard",
                            icon_url="https://cdn.discordapp.com/icons/943556434644328498/901cbfed0350db86feaee903637f477b.webp?size=240")
        await ctx.send(embed=embed)

@bot.event
async def on_reaction_add(reaction, user):
    if not user.bot: 
        if reaction.emoji == "🤍":
            await serious()
            try: 
                await reaction.message.delete()
                await tagEmbedMessage()
            except: 
                await tagEmbedMessage()
    if not user.bot: 
        if reaction.emoji == "🌻": 
            await casual()
            cofirm = await reaction.message.channel.send("Click on `Envelope` reaction to accept private messages on this vent. (Click on `☘️` if you dont want to accept private message on this vent)\n**Note:** Person who will send private message to you wont be able to know who you are and you wont be able to know who they are.")
            await cofirm.add_reaction("📩")
            await cofirm.add_reaction("☘️")
            try:
                await reaction.message.delete()
            except: 
                pass
    if not user.bot:
        if reaction.emoji == "📩":
            await accept()
            try:
                await reaction.message.delete()
            except: 
                pass
    if not user.bot:
        if reaction.emoji == "☘️":
            await cross()
            try:
                await reaction.message.delete()
            except: 
                pass

@bot.event
async def on_raw_reaction_add(payload):
    if not payload.member.bot:
        if payload.emoji.name == "🫂":
            if prof.find_one({"user": payload.member.id}):
                prof.update_one({"user": payload.member.id}, {"$inc": {"reputation": 1}})
            else: 
                post = {"user": payload.member.id, "reputation": 1}
                prof.insert_one(post)

        if payload.emoji.name == "🔍":
            channel = bot.get_channel(payload.channel_id)
            message = channel.get_partial_message(payload.message_id)
            await message.remove_reaction(payload.emoji ,payload.member)
            em = discord.Embed(
                description="No one can access this channel even server owners wont have a look on custom private vent channels because we respect privacy. You are here all by yourself so dont worry about getting judged and feel free to vent.\nWhatever you'll vent about here will be posted publicly on <#943556439195152477> channel but no one can know who typed it and what is their identity so feel safe.\n__Once you are done venting out, we will temporarily BLOCK you from sending any message here to avoid spams and trolls.__\n\n**Why keeping us anonymous?**\nWe try our best to help people across the globe to deal with whatever they are going through.\nSince many people on the internet are insecure about getting judged and dealing with toxicity online, we try to minimize it by keeping you anonymous.\n\n**Why are we doing this?**\nWe understand how tough life can get and we understand it can be really difficult for one to go through all the pain and sufferings.\nAll we want is you to move forward in life and this effort is a little push to that. We want to let you know that you are not alone in this game, a lot of people on the world share similar pain. (knowing this definitely helps one to move forward)\n\nSometimes it is better to let your heart cry out loud in a place where no one will judge you, and that is where this server comes in play."
            )
            em.set_author(name="Information: ",
                          icon_url="https://cdn.discordapp.com/icons/943556434644328498/901cbfed0350db86feaee903637f477b.webp?size=240")
            channel = bot.get_channel(payload.channel_id)
            txt = await channel.fetch_message(payload.message_id)
            await txt.edit(embed=em)
            await txt.add_reaction('⬅️')
        if payload.emoji.name == '⬅️':
            channel = bot.get_channel(payload.channel_id)
            message = channel.get_partial_message(payload.message_id)
            await message.remove_reaction(payload.emoji ,payload.member)
            ema = discord.Embed(
                description="1) Make your text fit in one single message because you will be locked out for \n`2 Hours` after you vent to prevent spams.\n\n2) Dm <@962603846696337408> to get your message deleted or edited (A staff member will assist you).\n\n3) You can DM <@962603846696337408> bot for any help related to the server.\n\nPlease vent here in this channel and not in bot's DM.\n__React with 🔍 emoji for more information__"
            )
            ema.set_author(name="Instruction: ",
                           icon_url="https://cdn.discordapp.com/icons/943556434644328498/901cbfed0350db86feaee903637f477b.webp?size=240")
            ema.set_footer(
                text="Note: We dont save your details and message in any separate database.")
            channel = bot.get_channel(payload.channel_id)
            txt = await channel.fetch_message(payload.message_id) 
            await txt.edit(embed=ema)
            await txt.add_reaction('🔍')
        if payload.emoji.name == "💬":
            if prof.find_one({"user": payload.member.id}):
                prof.update_one({"user": payload.member.id}, {"$inc": {"reputation": 1}})
            else: 
                post = {"user": payload.member.id, "reputation": 1}
                prof.insert_one(post)

            channel = bot.get_channel(payload.channel_id)
            message = channel.get_partial_message(payload.message_id)
            await message.remove_reaction(payload.emoji ,payload.member)
            if collection.find_one({"msg_id": payload.message_id}):
                db_data = collection.find_one({"msg_id": payload.message_id})
                #guild = payload.guild_id
                guild = bot.get_guild(payload.guild_id)
                user_a = payload.member
                #role_b = discord.utils.get(user.guild.roles, name="Blocked")
                server = bot.get_guild(943556434644328498)
                msg_owner = server.get_member(int(db_data["author_id"]))
                if msg_owner is None: 
                    await user_a.send("Vent message owner not found! They probably left the server.")
                else:
                    
                    # print(msg_owner)
                    #print(f"msg_owner: {msg_owner}")
                    #print(f"user_a: {user_a}")

                    characters = '1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
                    inboxCode = "".join(choice(characters)
                                    for x in range(randint(2, 5)))

                    try: 
                        categOwner = discord.utils.get(guild.categories, name="📨 INBOX")

                        text_channel_replier = await categOwner.create_text_channel(f"{inboxCode}")

                        await text_channel_replier.set_permissions(user_a, send_messages=True, view_channel=True)
                        await text_channel_replier.set_permissions(msg_owner, view_channel=False)
                        await text_channel_replier.set_permissions(guild.default_role, send_messages=False, view_channel=False)
                        binEmbed = discord.Embed(description="Use `.bin` command here to close this inbox", colour=discord.Colour.red())
                        await text_channel_replier.send(f"You can send your message here and it will be sent to the author automatically! <@{payload.member.id}>", embed = binEmbed)
                        #collection.update_one({"msg_id": reaction.message.id}, {"$set":{f"inbox{user.discriminator}":text_channel_replier.id}})

                        # await text_channel_replier.set_permissions(role_b, send_messages=False)
                        text_channel_owner = await categOwner.create_text_channel(f"{inboxCode}")

                        await text_channel_owner.set_permissions(user_a, view_channel=False)
                        await text_channel_owner.set_permissions(msg_owner, send_messages=True, view_channel=True)
                        await text_channel_owner.set_permissions(guild.default_role, send_messages=False, view_channel=False)
                        await text_channel_owner.edit(topic=f"{str(text_channel_replier.id)}")
                        await text_channel_replier.edit(topic=f"{str(text_channel_owner.id)}")
                        #await text_channel_owner.send(f"Someone wants to talk to you about {db_data['msg_link']}. You'll recieve their message here and you can reply to it by texting here. <@{db_data['author_id']}>", embed = binEmbed)

                        txt = await channel.fetch_message(payload.message_id)
                        ventMsg = discord.Embed(description=f"{txt.embeds[0].description}")
                        ventMsg.set_author(name="Anonymous", icon_url="https://res.cloudinary.com/teepublic/image/private/s--UymRXkch--/t_Resized%20Artwork/c_fit,g_north_west,h_1054,w_1054/co_ffffff,e_outline:53/co_ffffff,e_outline:inner_fill:53/co_bbbbbb,e_outline:3:1000/c_mpad,g_center,h_1260,w_1260/b_rgb:eeeeee/c_limit,f_auto,h_630,q_90,w_630/v1570281377/production/designs/6215195_0.jpg")
                        await text_channel_owner.send(f"Someone wants to talk to you about your vent. You'll recieve their message here and you can reply to it by texting here. <@{db_data['author_id']}>", embed = ventMsg)
                        await text_channel_owner.send(embed=binEmbed)
                    except:
                        try: 
                            categOwner = discord.utils.get(guild.categories, name="📨 INBOX (2)")

                            text_channel_replier = await categOwner.create_text_channel(f"{inboxCode}")

                            await text_channel_replier.set_permissions(user_a, send_messages=True, view_channel=True)
                            await text_channel_replier.set_permissions(msg_owner, view_channel=False)
                            await text_channel_replier.set_permissions(guild.default_role, send_messages=False, view_channel=False)
                            binEmbed = discord.Embed(description="Use `.bin` command here to close this inbox", colour=discord.Colour.red())
                            await text_channel_replier.send(f"You can send your message here and it will be sent to the author automatically! <@{payload.member.id}>", embed = binEmbed)
                            #collection.update_one({"msg_id": reaction.message.id}, {"$set":{f"inbox{user.discriminator}":text_channel_replier.id}})

                            # await text_channel_replier.set_permissions(role_b, send_messages=False)
                            text_channel_owner = await categOwner.create_text_channel(f"{inboxCode}")

                            await text_channel_owner.set_permissions(user_a, view_channel=False)
                            await text_channel_owner.set_permissions(msg_owner, send_messages=True, view_channel=True)
                            await text_channel_owner.set_permissions(guild.default_role, send_messages=False, view_channel=False)
                            await text_channel_owner.edit(topic=f"{str(text_channel_replier.id)}")
                            await text_channel_replier.edit(topic=f"{str(text_channel_owner.id)}")

                            txt = await channel.fetch_message(payload.message_id)
                            ventMsg = discord.Embed(description=f"{txt.embeds[0].description}")
                            ventMsg.set_author(name="Anonymous", icon_url="https://res.cloudinary.com/teepublic/image/private/s--UymRXkch--/t_Resized%20Artwork/c_fit,g_north_west,h_1054,w_1054/co_ffffff,e_outline:53/co_ffffff,e_outline:inner_fill:53/co_bbbbbb,e_outline:3:1000/c_mpad,g_center,h_1260,w_1260/b_rgb:eeeeee/c_limit,f_auto,h_630,q_90,w_630/v1570281377/production/designs/6215195_0.jpg")
                            await text_channel_owner.send(f"Someone wants to talk to you about your vent. You'll recieve their message here and you can reply to it by texting here. <@{db_data['author_id']}>", embed = ventMsg)
                            await text_channel_owner.send(embed=binEmbed)
                        except: 
                            categOwner = discord.utils.get(guild.categories, name="📨 INBOX (3)")

                            text_channel_replier = await categOwner.create_text_channel(f"{inboxCode}")

                            await text_channel_replier.set_permissions(user_a, send_messages=True, view_channel=True)
                            await text_channel_replier.set_permissions(msg_owner, view_channel=False)
                            await text_channel_replier.set_permissions(guild.default_role, send_messages=False, view_channel=False)
                            binEmbed = discord.Embed(description="Use `.bin` command here to close this inbox", colour=discord.Colour.red())
                            await text_channel_replier.send(f"You can send your message here and it will be sent to the author automatically! <@{payload.member.id}>", embed = binEmbed)
                            #collection.update_one({"msg_id": reaction.message.id}, {"$set":{f"inbox{user.discriminator}":text_channel_replier.id}})

                            # await text_channel_replier.set_permissions(role_b, send_messages=False)
                            text_channel_owner = await categOwner.create_text_channel(f"{inboxCode}")

                            await text_channel_owner.set_permissions(user_a, view_channel=False)
                            await text_channel_owner.set_permissions(msg_owner, send_messages=True, view_channel=True)
                            await text_channel_owner.set_permissions(guild.default_role, send_messages=False, view_channel=False)
                            await text_channel_owner.edit(topic=f"{str(text_channel_replier.id)}")
                            await text_channel_replier.edit(topic=f"{str(text_channel_owner.id)}")

                            txt = await channel.fetch_message(payload.message_id)
                            ventMsg = discord.Embed(description=f"{txt.embeds[0].description}")
                            ventMsg.set_author(name="Anonymous", icon_url="https://res.cloudinary.com/teepublic/image/private/s--UymRXkch--/t_Resized%20Artwork/c_fit,g_north_west,h_1054,w_1054/co_ffffff,e_outline:53/co_ffffff,e_outline:inner_fill:53/co_bbbbbb,e_outline:3:1000/c_mpad,g_center,h_1260,w_1260/b_rgb:eeeeee/c_limit,f_auto,h_630,q_90,w_630/v1570281377/production/designs/6215195_0.jpg")
                            await text_channel_owner.send(f"Someone wants to talk to you about your vent. You'll recieve their message here and you can reply to it by texting here. <@{db_data['author_id']}>", embed = ventMsg)
                            await text_channel_owner.send(embed=binEmbed)

                    # Inserting Inbox information in the DataBase
                    post={"channel":f"{inboxCode}", "reactor":payload.member.id, "author":int(db_data["author_id"])}
                    inbox.insert_one(post)

            else:
                print('Cannot find message id in DataBase!')
                await payload.member.send('Vent author left the server!')

########### Error Handling ##########
@bot.event
async def on_command_error(ctx, error):
    em = discord.Embed(description=f"Command: `{ctx.command}`\n```{error}```")
    await ctx.send(embed=em)
    raise error
#####################################

asyncio.run(main())