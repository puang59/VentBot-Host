from discord.ext import commands
import discord
import asyncio

from pymongo import MongoClient
from random import *
# import configparser

import time
import datetime

from ._logger import _logger

class _events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # config = configparser.ConfigParser()
    # config.read('_ventV2.0/config.ini')

    global collection
    global prof
    global inbox
    global vType
    global vCheck
    global stories
    cluster = MongoClient("mongodb+srv://Edryu:jaisairam4@cluster0.inbe1.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = cluster["Discord"]
    collection = db["vent"]
    
    prof = db["ventProf"]
    inbox = db['ventInbox']
    inboxDating = db['DatingInbox']
    vCheck = db["ventCheck"]
    stories = db['webVent']
    vType = db['ventType']


    global logger
    logger = _logger(commands.Bot)

    #################### BUTTONS ####################


    global cofirm   
    global tagButtons
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
            vCheck.update_one({"user": interaction.user.id}, {"$set": {"tags": " "}})
            button.disabled=True
            button.label="None" 
            cofirm = await interaction.channel.send("`📩` - Accept Private Anonymous Message\n`☘️` - Do not accept private anonymous message\n\n**Note:** Person who will send private message to you wont be able to know who you are and you wont be able to know who they are.")
            await cofirm.add_reaction("📩")
            await cofirm.add_reaction("☘️")
            await interaction.response.edit_message(view=self)
            await interaction.message.delete()
        @discord.ui.button(label="Done",style=discord.ButtonStyle.green, disabled=False, emoji='👍')
        async def done_button(self, interaction:discord.Interaction, button:discord.ui.Button):
            button.disabled=True
            button.label="Done"
            cofirm = await interaction.channel.send("`📩` - Accept Private Anonymous Message\n`☘️` - Do not accept private anonymous message\n\n**Note:** Person who will send private message to you wont be able to know who you are and you wont be able to know who they are.")
            await cofirm.add_reaction("📩")
            await cofirm.add_reaction("☘️")
            await interaction.response.edit_message(view=self)
            await interaction.message.delete()

    global ReportBtn
    class ReportBtn(discord.ui.View):
        def __init__(self, *, timeout=3600):
            super().__init__(timeout=timeout)
            self.bot = bot

        @discord.ui.button(label="Report User",style=discord.ButtonStyle.danger, disabled=False)
        async def gray_button(self, interaction:discord.Interaction, button:discord.ui.Button):
            button.disabled=True
            button.label="Reported"
            button.style=discord.ButtonStyle.gray
            await interaction.response.edit_message(view=self)
            channel = self.bot.get_channel(943909084430729217)
            if inbox.find_one({"reactor":interaction.user.id}):
                data = inbox.find_one({"reactor":interaction.user.id})
                author = self.bot.get_user(int(data['author']))

                interChn = self.bot.get_channel(interaction.channel_id)
                txt = await interChn.fetch_message(interaction.message.id)
                em = discord.Embed(description=f"{txt.embeds[0].description}")

                em.set_author(name=f"{author.name} - {data['author']}", icon_url=f"{author.avatar.url}")
                await channel.send(f"{interaction.channel.name} - <#{interaction.channel_id}>", embed=em)
                await interaction.channel.send(content="<:agree:943603027313565757> The user has been reported to the staff team.")
                #blocking the reported user 
                topic = interaction.channel.topic
                chn = interaction.guild.get_channel(int(topic))
                await chn.edit(topic=f"{chn.topic}"+" REPORTED")
                await interaction.channel.edit(topic=f"{interaction.channel.topic}"+" Reporter")
                await chn.send("You have been reported by the person your were talking to! We are looking into the matter and will get back to you soon.")
            elif inbox.find_one({"author":interaction.user.id}):
                data = inbox.find_one({"author":interaction.user.id})
                reactor = self.bot.get_user(int(data['reactor']))

                interChn = self.bot.get_channel(interaction.channel_id)
                txt = await interChn.fetch_message(interaction.message.id)
                em = discord.Embed(description=f"{txt.embeds[0].description}")

                em.set_author(name=f"{reactor.name} - {data['reactor']}", icon_url=f"{reactor.avatar.url}")
                await channel.send(f"{interaction.channel.name} - <#{interaction.channel_id}>", embed=em)
                await interaction.channel.send(content="<:agree:943603027313565757> The user has been reported to the staff team.")
                topic = interaction.channel.topic
                chn = interaction.guild.get_channel(int(topic))
                await chn.edit(topic=f"{chn.topic}"+" REPORTED")
                await interaction.channel.edit(topic=f"{interaction.channel.topic}"+" Reporter")
                await chn.send("You have been reported by the person your were talking to! We are looking into the matter and will get back to you soon.")
            else: 
                await interaction.channel.send("UhOh! Looks like something went wrong. Please DM me to report the user instead.")

    #################################################


    @commands.Cog.listener()
    async def on_message(self, msg):  
        if not msg.author.bot:
            t = time.localtime()
            current_time = time.strftime("%H:%M", t)
            print(f"[{msg.author.name}][{msg.channel.name}][{current_time}] - {msg.content}")
            if not msg.content.startswith(self.bot.command_prefix):
                if not isinstance(msg.channel, discord.channel.DMChannel):
                    if msg.channel.category.id in [943581279973167155, 987993408138248243, 987993582701019166, 996458874255187978, 996459675589554206]:
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
                            if not msg.content.startswith(self.bot.command_prefix): #checking if msg is a commands 
                                if len(msg.clean_content) < 10:
                                    x = await msg.channel.send("<:disagree:943603027854626816> Your message is too small. (Message should have more than 10 characters)")
                                    await asyncio.sleep(10)
                                    await x.delete()
                                else:
                                    characters = '1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
                                    msg_code = "".join(choice(characters)
                                                    for x in range(randint(4, 10)))

                                    member = msg.author
                                    if msg.author.id == 852797584812670996:
                                        pass
                                    else:
                                        role = discord.utils.get(
                                            msg.guild.roles, name="Blocked")

                                    vent_channel = self.bot.get_channel(943556439195152477)
                                    casual_channel = self.bot.get_channel(1014201909118251098)
                                    help_channel = self.bot.get_channel(1035490966934659093)

                                    typeMsg = await msg.channel.send("```Select vent type:```\n`🤍` - <#943556439195152477>\n`🌻` - <#1014201909118251098>\n`📮` - <#1035490966934659093>")
                                    await typeMsg.add_reaction('🤍')
                                    await typeMsg.add_reaction('🌻')
                                    await typeMsg.add_reaction('📮')

                                    global casual 
                                    async def casual(): 
                                        post = {"author_id": msg.author.id, "msg_id": msg.id, "type": "casual"}
                                        vType.insert_one(post)
                                    
                                    global serious 
                                    async def serious(): 
                                        post = {"author_id": msg.author.id, "msg_id": msg.id, "type": "serious"}
                                        vType.insert_one(post)

                                    global helpchn 
                                    async def helpchn():
                                        post = {"author_id": msg.author.id, "msg_id": msg.id, "type": "help"}
                                        vType.insert_one(post)

                                    global tagEmbedMessage
                                    async def tagEmbedMessage():
                                        vCheck.insert_one({"user": msg.author.id, "tags": "> "})
                                        tagEm = discord.Embed(
                                            description=f"Click on the tags (press 'None' if you want no tag) and when you are done, press 'Done' button\n**Note:** You can select multiple tags."
                                        )
                                        tagEm.set_author(name="Choose Tags", icon_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fcdn1.iconfinder.com%2Fdata%2Ficons%2Fhawcons%2F32%2F698889-icon-146-tag-512.png&f=1&nofb=1")
                                        await msg.channel.send(embed=tagEm, view=tagButtons())
                                    
                                    global cross
                                    async def cross():
                                        tagData = vCheck.find_one({"user": msg.author.id})
                                        ventTypeCheck = vType.find_one({'author_id': msg.author.id})
                                        try: 
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
                                        except: 
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

                                        #logger.logInput('type', f"{ventTypeCheck['type']}")
                                        vType.delete_many({'author_id':msg.author.id})
                                        vCheck.delete_many({'user': msg.author.id})
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

                                        print(f"---------- NEW VENT RECORDED {datetime.datetime.utcnow().time()} UTC ----------")
                                        ########## LOGGING ##########
                                        #logger.logInput('at', "null")
                                        #logger.logInput('by', f"{msg.author.name}")
                                        #try: 
                                        #    logger.logInput('messageid', f"{x.id}")
                                        #except: 
                                        #    logger.logInput('messageid', f"{y.id}")

                                    global accept

                                    async def accept():
                                        tagData = vCheck.find_one({"user": msg.author.id})
                                        ventTypeCheck = vType.find_one({'author_id': msg.author.id})
                                        # check if tag is empty - if yes then remove tags from embed - if no then continue
                                        try: 
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
                                        except: 
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
                                        elif ventTypeCheck['type'] == "casual": 
                                            y = await casual_channel.send(embed=em)
                                            await y.add_reaction('🗣')
                                            await y.add_reaction('💬')
                                        elif ventTypeCheck['type'] == "help": 
                                            z = await help_channel.send(embed=em)
                                            await z.add_reaction('⬆️')
                                            await z.add_reaction('💬')
                                        #logger.logInput('type', f"{ventTypeCheck['type']}")
                                        vType.delete_many({'author_id':msg.author.id})
                                        vCheck.delete_many({'user': msg.author.id})
                                        stories.update_one({"guild": "vent"}, {"$inc": {"stories": 1}})

                                        try: 
                                            try: 
                                                post = {"author_id": msg.author.id, "code": f"{msg_code}",
                                                        "msg_link": f"{x.jump_url}", "msg_id": x.id, "channel_id": msg.channel.id, "owner_name": f"{msg.author.name}#{msg.author.discriminator}", "ident": "vent"}
                                                collection.insert_one(post)
                                            except: 
                                                post = {"author_id": msg.author.id, "code": f"{msg_code}",
                                                        "msg_link": f"{y.jump_url}", "msg_id": y.id, "channel_id": msg.channel.id, "owner_name": f"{msg.author.name}#{msg.author.discriminator}", "ident": "vent"}
                                                collection.insert_one(post)
                                        except: 
                                            post = {"author_id": msg.author.id, "code": f"{msg_code}",
                                                    "msg_link": f"{z.jump_url}", "msg_id": z.id, "channel_id": msg.channel.id, "owner_name": f"{msg.author.name}#{msg.author.discriminator}", "ident": "vent"}
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
                                        print(f"---------- NEW VENT RECORDED {datetime.datetime.utcnow().time()} UTC ----------")
                                        ########## LOGGING ##########
                                        #logger.logInput('at', "null")
                                        #logger.logInput('by', f"{msg.author.name}")
                                        #try: 
                                        #    try: 
                                        #        logger.logInput('messageid', f"{x.id}")
                                        #    except: 
                                        #        logger.logInput('messageid', f"{y.id}")
                                        #except: 
                                        #    logger.logInput('messageid', f"{z.id}")

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

                #await self.bot.process_commands(msg)


    #################### REACTION MONITOR ####################


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        try: 
            if not payload.member.bot:
                if payload.emoji.name == "🫂":
                    if prof.find_one({"user": payload.member.id}):
                        prof.update_one({"user": payload.member.id}, {"$inc": {"reputation": 1}})
                    else: 
                        post = {"user": payload.member.id, "reputation": 1}
                        prof.insert_one(post)

                if payload.emoji.name == "🔍":
                    channel = self.bot.get_channel(payload.channel_id)
                    message = channel.get_partial_message(payload.message_id)
                    await message.remove_reaction(payload.emoji ,payload.member)
                    em = discord.Embed(
                        description="No one can access this channel even server owners wont have a look on custom private vent channels because we respect privacy. You are here all by yourself so dont worry about getting judged and feel free to vent.\nWhatever you'll vent about here will be posted publicly on either <#943556439195152477>  or <#1014201909118251098> channel (you can decide when you vent) but no one can know who typed it and what is their identity so feel safe.\n__Once you are done venting out, we will temporarily BLOCK you from sending any message here to avoid spams and trolls.__\n\n**Why keeping us anonymous?**\nWe try our best to help people across the globe to deal with whatever they are going through.\nSince many people on the internet are insecure about getting judged and dealing with toxicity online, we try to minimize it by keeping you anonymous.\n\n**Why are we doing this?**\nWe understand how tough life can get and we understand it can be really difficult for one to go through all the pain and sufferings.\nAll we want is you to move forward in life and this effort is a little push to that. We want to let you know that you are not alone in this game, a lot of people on the world share similar pain. (knowing this definitely helps one to move forward)\n\nSometimes it is better to let your heart cry out loud in a place where no one will judge you, and that is where this server comes in play."
                    )
                    em.set_author(name="Information: ",
                                icon_url="https://cdn.discordapp.com/icons/943556434644328498/901cbfed0350db86feaee903637f477b.webp?size=240")
                    channel = self.bot.get_channel(payload.channel_id)
                    txt = await channel.fetch_message(payload.message_id)
                    await txt.edit(embed=em)
                    await txt.add_reaction('⬅️')
                if payload.emoji.name == '⬅️':
                    channel = self.get_channel(payload.channel_id)
                    message = channel.get_partial_message(payload.message_id)
                    await message.remove_reaction(payload.emoji ,payload.member)
                    ema = discord.Embed(
                        description="1) Make your text fit in one single message because you will be locked out for \n`2 Hours` after you vent to prevent spams.\n\n2) Dm <@962603846696337408> to get your message deleted or edited (A staff member will assist you).\n\n3) You can DM <@962603846696337408> bot for any help related to the server.\n\nPlease vent here in this channel and not in bot's DM.\n__React with 🔍 emoji for more information__"
                    )
                    ema.set_author(name="Instruction: ",
                                icon_url="https://cdn.discordapp.com/icons/943556434644328498/901cbfed0350db86feaee903637f477b.webp?size=240")
                    ema.set_footer(
                        text="Note: We dont save your details and message in any separate database.")
                    channel = self.bot.get_channel(payload.channel_id)
                    txt = await channel.fetch_message(payload.message_id) 
                    await txt.edit(embed=ema)
                    await txt.add_reaction('🔍')
                if payload.emoji.name == "💬":
                    if prof.find_one({"user": payload.member.id}):
                        prof.update_one({"user": payload.member.id}, {"$inc": {"reputation": 1}})
                    else: 
                        post = {"user": payload.member.id, "reputation": 1}
                        prof.insert_one(post)

                    channel = self.bot.get_channel(payload.channel_id)
                    message = channel.get_partial_message(payload.message_id)
                    await message.remove_reaction(payload.emoji ,payload.member)
                    if collection.find_one({"msg_id": payload.message_id}):
                        db_data = collection.find_one({"msg_id": payload.message_id})
                        #guild = payload.guild_id
                        guild = self.bot.get_guild(payload.guild_id)
                        user_a = payload.member
                        #role_b = discord.utils.get(user.guild.roles, name="Blocked")
                        server = self.bot.get_guild(943556434644328498)
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
        except: 
            pass

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
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
                cofirm = await reaction.message.channel.send("`📩` - Accept Private Anonymous Message\n`☘️` - Do not accept private anonymous message\n\n**Note:** Person who will send private message to you wont be able to know who you are and you wont be able to know who they are.")
                await cofirm.add_reaction("📩")
                await cofirm.add_reaction("☘️")
                try:
                    await reaction.message.delete()
                except: 
                    pass
        if not user.bot: 
            if reaction.emoji == "📮": 
                await helpchn()
                await reaction.message.delete()
                await accept()
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


    #################### MISC ####################
    
    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        guild = self.bot.get_guild(943556434644328498)
        if before.name != after.name: 
            try: 
                channel = discord.utils.get(guild.channels, name=f'{before.name}s-vent-{before.discriminator}')
                await channel.edit(name=f'{after.name}s-vent-{after.discriminator}')
            except: 
                channel = discord.utils.get(guild.channels, name=f'{before.name}s-vent')
                await channel.edit(name=f'{after.name}s-vent-{after.discriminator}')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.guild.id == 943556434644328498:
            guild = self.bot.get_guild(943556434644328498)
            leaveChannel = self.bot.get_channel(943909084430729217)
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
                if not member == None:
                    try: 
                        prof.delete_one({'user': int(member)})
                    except: 
                        await x.add_reaction('❌')


    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 943556434644328498:
            joinChannel = self.bot.get_channel(943909084430729217)
            em = discord.Embed(description=f"<:agree:943603027313565757> {member.name} ({member.id}) joined!", colour=discord.Colour.green())
            x = await joinChannel.send(embed=em)  

            try: 
                if not prof.find_one({"user": member.id}):
                    post = {"user": member.id, "reputation": 0}
                    prof.insert_one(post)

                if member.guild.id == 943556434644328498:
                    if collection.find_one({"author_id": member.id}):
                        data = collection.find_one({"author_id": member.id})
                        ch = self.bot.get_channel(int(data["channel_id"]))
                        await ch.set_permissions(member, send_messages=True, view_channel=True)
                    else:
                        guild = member.guild
                        user_a = member
                        role_b = discord.utils.get(member.guild.roles, name="Blocked")

                        categories = ["PRIVATE SPACE (1)", "PRIVATE SPACE (2)", "PRIVATE SPACE (3)","PRIVATE SPACE (4)","PRIVATE SPACE (5)",\
                                    "PRIVATE SPACE (6)","PRIVATE SPACE (7)", "PRIVATE SPACE (8)","PRIVATE SPACE (9)","PRIVATE SPACE (10)"]

                        for categName in categories:
                            try: 
                                categ = discord.utils.get(guild.categories, name=categName)
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
                                            icon_url=guild.icon)
                                ema.set_footer(
                                    text="Note: We dont save your details and message in any separate database.")
                                await text_channel.send(f"Welcome {member.mention}!  (≧◡≦)")
                                a = await text_channel.send(embed=ema)
                                await a.add_reaction('🔍')
                                break 
                            except: 
                                pass             
                await x.add_reaction('✔️')
            except:
                await x.add_reaction('❌')

async def setup(bot):
    await bot.add_cog(_events(bot))
