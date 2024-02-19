from discord.ext import commands, tasks
import discord
import asyncio

from pymongo import MongoClient
from random import *
# import configparser
from RoboArt import roboart
import time
import os
import datetime

import traceback 

import config

from ._logger import _logger

GUILD_ID = 943556434644328498

class _events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = None
        self.check_delete_channels.start()

    async def cog_load(self):
        self.conn = await self.bot.get_db_connection()

    global collection
    global prof
    global inbox
    global vType
    global vCheck
    global stories
    global logdb
    global ventUserId

    cluster = MongoClient(config.mongoURI)
    db = cluster["Discord"]

    collection = db["vent"]
    prof = db["ventProf"]
    inbox = db['ventInbox']
    vCheck = db["ventCheck"]
    stories = db['webVent']
    vType = db['ventType']
    logdb = db['ventLog']
    ventUserId = db['ventId']

    global logger
    logger = _logger(commands.Bot)

    @tasks.loop(seconds=120)  # Adjust the interval as needed
    async def check_delete_channels(self):
        guild = self.bot.get_guild(GUILD_ID)
        privatespace = discord.utils.get(guild.categories, name="YOUR PRIVATE SPACE")
        
        # Get the current time
        current_time = time.time()
        
        # Read channel creation times from the file
        channel_creation_times = {}
        if os.path.exists("channelLife.txt"):
            with open("channelLife.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    channel_id, creation_time = line.strip().split(",")
                    channel_creation_times[int(channel_id)] = float(creation_time)

        print(channel_creation_times) 

        # Iterate through text channels in the private space category
        for channel in privatespace.text_channels:
            channel_id = channel.id
            # Check if the channel exists in the creation times dictionary
            if channel_id in channel_creation_times:
                creation_time = channel_creation_times[channel_id]
                # Check if the channel has existed for more than 24 hours
                if current_time - creation_time >= 24 * 3600:  # 24 hours in seconds
                    # Delete the channel
                    try:
                        await channel.delete()
                    except:
                        pass
                    # Remove the channel's creation time from the dictionary and the file
                    del channel_creation_times[channel_id]
                    with open("channelLife.txt", "w") as file:
                        for ch_id, cr_time in channel_creation_times.items():
                            file.write(f"{ch_id},{cr_time}\n")

    @check_delete_channels.before_loop
    async def before_check_delete_channels(self):
        await self.bot.wait_until_ready()

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

        @discord.ui.button(label="Report User",style=discord.ButtonStyle.danger, disabled=False)
        async def gray_button(self, interaction:discord.Interaction, button:discord.ui.Button):
            button.disabled=True
            button.label="Reported"
            button.style=discord.ButtonStyle.gray
            await interaction.response.edit_message(view=self)
            #channel = self.bot.get_channel(943909084430729217)

            channel_id = 943909084430729217
            channel = discord.utils.get(interaction.guild.channels, id=channel_id)

            if inbox.find_one({"reactor":interaction.user.id}):
                data = inbox.find_one({"reactor":interaction.user.id})
                #author = self.bot.get_user(int(data['author']))

                authorId = int(data['author'])  # replace with the ID of the user you want to get
                author = discord.utils.get(interaction.guild.members, id=authorId)

                #interChn = self.bot.get_channel(interaction.channel_id)
                

                interChn_id = interaction.channel_id
                interChn = discord.utils.get(interaction.guild.channels, id=interChn_id)

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
                #reactor = self.bot.get_user(int(data['reactor']))

                reactorID = int(data['reactor'])  # replace with the ID of the user you want to get
                reactor = discord.utils.get(interaction.guild.members, id=reactorID)

                #interChn = self.bot.get_channel(interaction.channel_id)
                
                interChn_id = interaction.channel_id
                interChn = discord.utils.get(interaction.guild.channels, id=interChn_id)

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
                    # Increasing user reputation
                    query = """
                        INSERT INTO reputation (userID, rep)
                        VALUES ($1, $2)
                        ON CONFLICT (userID)
                        DO UPDATE SET rep = (reputation.rep + $2);
                    """

                    # yourprivatespace category id 
                    if msg.channel.category.id == 1208306210948775966:
                        reputation_value = 5
                    else:
                        reputation_value = 1

                    await self.conn.execute(query, msg.author.id, reputation_value)

            if not msg.author.id == 94392887341287015323: # anonimo user id
                if not isinstance(msg.channel, discord.channel.DMChannel):
                    if msg.channel.category.id == 1208306210948775966: #private space
                        if not msg.content.startswith(self.bot.command_prefix): #checking if msg is a commands 
                            # Storing unqiue user id
                            if not ventUserId.find_one({"user": msg.author.id}):
                                characters = '1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
                                uniqueId = "".join(choice(characters)
                                                for x in range(randint(20, 25)))
                                userSavePost = {"user": msg.author.id, "uniqueId": uniqueId}
                                ventUserId.insert_one(userSavePost)
                            else: 
                                pass

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
                                wok_channel = self.bot.get_channel(1108828942019858582)
                                
                                typeMsg = await msg.channel.send("```Select vent type:```\n`🤍` - <#943556439195152477>\n`🌻` - <#1014201909118251098>\n`📮` - <#1035490966934659093>\n----------\n`\U0001f48c` - <#1108828942019858582>")
                                await typeMsg.add_reaction('🤍')
                                await typeMsg.add_reaction('🌻')
                                await typeMsg.add_reaction('📮')
                                await typeMsg.add_reaction('\U0001f48c')

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


                                global wokchn 
                                async def wokchn():
                                    post = {"author_id": msg.author.id, "msg_id": msg.id, "type": "wok"}
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

                                    # Checking vent type
                                    if ventTypeCheck['type'] == "serious": 
                                        em.set_author(name="Anonymous", icon_url="https://res.cloudinary.com/teepublic/image/private/s--UymRXkch--/t_Resized%20Artwork/c_fit,g_north_west,h_1054,w_1054/co_ffffff,e_outline:53/co_ffffff,e_outline:inner_fill:53/co_bbbbbb,e_outline:3:1000/c_mpad,g_center,h_1260,w_1260/b_rgb:eeeeee/c_limit,f_auto,h_630,q_90,w_630/v1570281377/production/designs/6215195_0.jpg")
                                        x = await vent_channel.send(embed=em)
                                        await x.add_reaction('🫂')
                                        #await x.add_reaction('💬')
                                    elif ventTypeCheck['type'] == "casual": 
                                        em.set_author(name="Anonymous", icon_url="https://res.cloudinary.com/teepublic/image/private/s--UymRXkch--/t_Resized%20Artwork/c_fit,g_north_west,h_1054,w_1054/co_ffffff,e_outline:53/co_ffffff,e_outline:inner_fill:53/co_bbbbbb,e_outline:3:1000/c_mpad,g_center,h_1260,w_1260/b_rgb:eeeeee/c_limit,f_auto,h_630,q_90,w_630/v1570281377/production/designs/6215195_0.jpg")
                                        y = await casual_channel.send(embed=em)
                                        await y.add_reaction('🗣')
                                        #await y.add_reaction('💬')
                                    elif ventTypeCheck['type'] == "help": 
                                        em.set_author(name="Anonymous", icon_url="https://res.cloudinary.com/teepublic/image/private/s--UymRXkch--/t_Resized%20Artwork/c_fit,g_north_west,h_1054,w_1054/co_ffffff,e_outline:53/co_ffffff,e_outline:inner_fill:53/co_bbbbbb,e_outline:3:1000/c_mpad,g_center,h_1260,w_1260/b_rgb:eeeeee/c_limit,f_auto,h_630,q_90,w_630/v1570281377/production/designs/6215195_0.jpg")
                                        z = await help_channel.send(embed=em)
                                        await z.add_reaction('⬆️')
                                        #await z.add_reaction('💬')
                                    elif ventTypeCheck['type'] == "wok": 
                                        ra = roboart()
                                        authorname = str(msg.author.name)
                                        first_word = authorname.split()[0]
                                        em.set_author(name="Anonymous", icon_url=ra.kitten(f"{first_word}"))
                                        value = randint(0, 0xffffff)
                                        em.color = value 
                                        w = await wok_channel.send(embed=em)
                                        await w.add_reaction('\U0001f49e')

                                    #logger.logInput('type', f"{ventTypeCheck['type']}")
                                    vType.delete_many({'author_id':msg.author.id})
                                    vCheck.delete_many({'user': msg.author.id})
                                    stories.update_one({"guild": "vent"}, {"$inc": {"stories": 1}})

                                    uIdData = ventUserId.find_one({"user": msg.author.id})
                                    try: 
                                        try: 
                                            post = {"author_id": msg.author.id, "uniqueId": uIdData['uniqueId'], "code": f"{msg_code}",
                                                    "msg_link": f"{x.jump_url}", "msg_id": x.id, "channel_id": msg.channel.id, "owner_name": f"{msg.author.name}#{msg.author.discriminator}", "ident": "vent"}
                                            collection.insert_one(post)
                                        except: 
                                            post = {"author_id": msg.author.id,  "uniqueId": uIdData['uniqueId'], "code": f"{msg_code}",
                                                    "msg_link": f"{y.jump_url}", "msg_id": y.id, "channel_id": msg.channel.id, "owner_name": f"{msg.author.name}#{msg.author.discriminator}", "ident": "vent"}
                                            collection.insert_one(post)
                                    except:
                                        try: 
                                            post = {"author_id": msg.author.id, "uniqueId": uIdData['uniqueId'], "code": f"{msg_code}",
                                                    "msg_link": f"{z.jump_url}", "msg_id": z.id, "channel_id": msg.channel.id, "owner_name": f"{msg.author.name}#{msg.author.discriminator}", "ident": "vent"}
                                            collection.insert_one(post)    
                                        except:
                                            post = {"author_id": msg.author.id, "uniqueId": uIdData['uniqueId'], "code": f"{msg_code}",
                                                    "msg_link": f"{w.jump_url}", "msg_id": w.id, "channel_id": msg.channel.id, "owner_name": f"{msg.author.name}#{msg.author.discriminator}", "ident": "vent"}
                                            collection.insert_one(post)    
                                    try:
                                        await cofirm.delete()
                                    except:
                                        pass
                                    dataforlink = collection.find_one({"code": msg_code})
                                    linktodisplay = dataforlink['msg_link']

                                    # channel life
                                    with open("channelLife.txt", "r") as file:
                                        lines = file.readlines()
                                    channel_id_to_remove = msg.channel.id

                                    new_lines = [line for line in lines if not line.startswith(str(channel_id_to_remove))]

                                    with open("channelLife.txt", "w") as file:
                                        file.writelines(new_lines)

                                    # user channel 
                                    with open("userChannel.txt", "r") as file:
                                        lines = file.readlines()
                                    user_id_to_remove = msg.author.id 

                                    new_lines = [line for line in lines if not line.startswith(str(user_id_to_remove))]

                                    with open("userChannel.txt", "w") as file:
                                        file.writelines(new_lines)

                                    await msg.channel.delete()

                                    # await msg.reply(f"<:agree:943603027313565757> ||{msg_code}|| - is your message code. __Keep it safe somewhere and dont share.__\n \
                                    #                 {linktodisplay}")
                                    
                                    try:
                                        data = collection.find_one(
                                            {"code": msg_code})
                                        link = data["msg_link"]
                                        emdm = discord.Embed(
                                            description=f"||{msg_code}|| - {link}")
                                        await msg.author.send("<:agree:943603027313565757> Your vent was posted successfully! Heres the vent link with token just incase.", embed=emdm)
                                    except:
                                        print("DMs closed")

                                    logs = self.bot.get_channel(1089639606091259994)
                                    print(f"---------- NEW VENT RECORDED {datetime.datetime.utcnow().time()} UTC ----------")
                                    logsEmbed = discord.Embed(
                                        description=f"```NEW VENT RECORDED {datetime.datetime.utcnow().time()} UTC```\n \
                                            {linktodisplay}"
                                    )
                                    await logs.send(embed = logsEmbed)
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

                                    em.set_footer(
                                        text="You can click on speech-bubble emoji to reply to this vent and talk to the author anonymously.", icon_url="https://kidsattennis.ca/wp-content/uploads/2020/05/greenball.png")
                                    
                                    # Checking vent type
                                    if ventTypeCheck['type'] == "serious": 
                                        em.set_author(name="Anonymous", icon_url="https://res.cloudinary.com/teepublic/image/private/s--UymRXkch--/t_Resized%20Artwork/c_fit,g_north_west,h_1054,w_1054/co_ffffff,e_outline:53/co_ffffff,e_outline:inner_fill:53/co_bbbbbb,e_outline:3:1000/c_mpad,g_center,h_1260,w_1260/b_rgb:eeeeee/c_limit,f_auto,h_630,q_90,w_630/v1570281377/production/designs/6215195_0.jpg")
                                        x = await vent_channel.send(embed=em)
                                        await x.add_reaction('🫂')
                                        await x.add_reaction('💬')
                                    elif ventTypeCheck['type'] == "casual": 
                                        em.set_author(name="Anonymous", icon_url="https://res.cloudinary.com/teepublic/image/private/s--UymRXkch--/t_Resized%20Artwork/c_fit,g_north_west,h_1054,w_1054/co_ffffff,e_outline:53/co_ffffff,e_outline:inner_fill:53/co_bbbbbb,e_outline:3:1000/c_mpad,g_center,h_1260,w_1260/b_rgb:eeeeee/c_limit,f_auto,h_630,q_90,w_630/v1570281377/production/designs/6215195_0.jpg")
                                        y = await casual_channel.send(embed=em)
                                        await y.add_reaction('🗣')
                                        await y.add_reaction('💬')
                                    elif ventTypeCheck['type'] == "help": 
                                        em.set_author(name="Anonymous", icon_url="https://res.cloudinary.com/teepublic/image/private/s--UymRXkch--/t_Resized%20Artwork/c_fit,g_north_west,h_1054,w_1054/co_ffffff,e_outline:53/co_ffffff,e_outline:inner_fill:53/co_bbbbbb,e_outline:3:1000/c_mpad,g_center,h_1260,w_1260/b_rgb:eeeeee/c_limit,f_auto,h_630,q_90,w_630/v1570281377/production/designs/6215195_0.jpg")
                                        z = await help_channel.send(embed=em)
                                        await z.add_reaction('⬆️')
                                        await z.add_reaction('💬')
                                    elif ventTypeCheck['type'] == "wok": 
                                        ra = roboart() 
                                        authorname = str(msg.author.name)
                                        first_word = authorname.split()[0]
                                        em.set_author(name="Anonymous", icon_url=ra.kitten(f"{first_word}"))
                                        value = randint(0, 0xffffff)
                                        em.color = value 
                                        w = await wok_channel.send(embed=em)
                                        await w.add_reaction('\U0001f49e')
                                        await w.add_reaction('💬')

                                    #logger.logInput('type', f"{ventTypeCheck['type']}")
                                    vType.delete_many({'author_id':msg.author.id})
                                    vCheck.delete_many({'user': msg.author.id})
                                    stories.update_one({"guild": "vent"}, {"$inc": {"stories": 1}})

                                    uIdData = ventUserId.find_one({"user": msg.author.id})
                                    try: 
                                        try: 
                                            post = {"author_id": msg.author.id, "uniqueId": uIdData['uniqueId'], "code": f"{msg_code}",
                                                    "msg_link": f"{x.jump_url}", "msg_id": x.id, "channel_id": msg.channel.id, "owner_name": f"{msg.author.name}#{msg.author.discriminator}", "ident": "vent"}
                                            collection.insert_one(post)
                                        except: 
                                            post = {"author_id": msg.author.id, "uniqueId": uIdData['uniqueId'], "code": f"{msg_code}",
                                                    "msg_link": f"{y.jump_url}", "msg_id": y.id, "channel_id": msg.channel.id, "owner_name": f"{msg.author.name}#{msg.author.discriminator}", "ident": "vent"}
                                            collection.insert_one(post)
                                    except: 
                                        try: 
                                            post = {"author_id": msg.author.id, "uniqueId": uIdData['uniqueId'], "code": f"{msg_code}",
                                                    "msg_link": f"{z.jump_url}", "msg_id": z.id, "channel_id": msg.channel.id, "owner_name": f"{msg.author.name}#{msg.author.discriminator}", "ident": "vent"}
                                            collection.insert_one(post)    
                                        except:
                                            post = {"author_id": msg.author.id, "uniqueId": uIdData['uniqueId'], "code": f"{msg_code}",
                                                    "msg_link": f"{w.jump_url}", "msg_id": w.id, "channel_id": msg.channel.id, "owner_name": f"{msg.author.name}#{msg.author.discriminator}", "ident": "vent"}
                                            collection.insert_one(post)    

                                    try:
                                        await cofirm.delete()
                                    except:
                                        pass
                                    dataforlink = collection.find_one({"code": msg_code})
                                    linktodisplay = dataforlink['msg_link']

                                    # channel life
                                    with open("channelLife.txt", "r") as file:
                                        lines = file.readlines()
                                    channel_id_to_remove = msg.channel.id

                                    new_lines = [line for line in lines if not line.startswith(str(channel_id_to_remove))]

                                    with open("channelLife.txt", "w") as file:
                                        file.writelines(new_lines)

                                    # user channel 
                                    with open("userChannel.txt", "r") as file:
                                        lines = file.readlines()
                                    user_id_to_remove = msg.author.id 

                                    new_lines = [line for line in lines if not line.startswith(str(user_id_to_remove))]

                                    with open("userChannel.txt", "w") as file:
                                        file.writelines(new_lines)

                                    await msg.channel.delete()

                                    # await msg.reply(f"<:agree:943603027313565757> ||{msg_code}|| - is your message code. __Keep it safe somewhere and dont share.__\n \
                                    #                 {linktodisplay}")

                                    try:
                                        data = collection.find_one(
                                            {"code": msg_code})
                                        link = data["msg_link"]
                                        emdm = discord.Embed(
                                            description=f"||{msg_code}|| - {link}")
                                        await msg.author.send("<:agree:943603027313565757> Your vent was posted successfully! Heres the vent link with token just incase.", embed=emdm)
                                    except:
                                        print("DMs closed")
                                    
                                    logs = self.bot.get_channel(1089639606091259994)
                                    print(f"---------- NEW VENT RECORDED {datetime.datetime.utcnow().time()} UTC ----------")
                                    logsEmbed = discord.Embed(
                                        description=f"```NEW VENT RECORDED {datetime.datetime.utcnow().time()} UTC```\n \
                                            {linktodisplay}"
                                    )
                                    await logs.send(embed = logsEmbed)

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
                if payload.emoji.name == "\U0001f4dd": # private space creation
                    if payload.channel_id == 1208306336392290324:
                        # create channel here 
                        channel = self.bot.get_channel(payload.channel_id)
                        message = channel.get_partial_message(payload.message_id)
                        await message.remove_reaction(payload.emoji ,payload.member)

                        # Read the userChannel.txt file
                        with open("userChannel.txt", "r") as file:
                            lines = file.readlines()

                        # Check if the user ID is stored in the file
                        user_id_to_check = str(payload.user_id)
                        for line in lines:
                            user_id, channel_id = line.strip().split(",")
                            if user_id == user_id_to_check:
                                await payload.member.send(f"Your channel is already active - <#{channel_id}>")
                                return

                        guild = self.bot.get_guild(payload.guild_id)
                        privatespace = discord.utils.get(guild.categories, name="YOUR PRIVATE SPACE")

                        characters = '1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
                        randomId= "".join(choice(characters)
                                        for x in range(randint(20, 25)))
                        text_channel = await privatespace.create_text_channel(f"{payload.member.name}s vent {randomId[0:7]}") 

                        await text_channel.set_permissions(payload.member, send_messages=True, view_channel=True)
                        await text_channel.set_permissions(guild.default_role, send_messages=False, view_channel=False)
                        await text_channel.edit(topic=f"Custom PRIVATE Vent channel for {payload.member.name}")
                        await text_channel.edit(slowmode_delay=7200)

                        ema = discord.Embed(
                            description="1) Make your text fit in one single message because the channel will be deleted once your vent is posted in public channels.\n\n2) Dm <@962603846696337408> to get your message deleted or edited (A staff member will assist you).\n\n3) You can DM <@962603846696337408> bot for any help related to the server.\n\nPlease vent here in this channel and not in bot's DM.\n__React with 🔍 emoji for more information__"
                        )
                        ema.set_author(name="Instruction: ",
                                    icon_url=guild.icon)
                        ema.set_footer(
                            text="Note: We dont save your details and message in any separate database.")
                        await text_channel.send(f"Welcome {payload.member.mention}!  (≧◡≦)")
                        a = await text_channel.send(embed=ema)
                        await a.add_reaction('🔍')

                        # Store channel ID and creation time in the file
                        try:
                            with open("channelLife.txt", "a") as file:
                                file.write(f"{text_channel.id},{time.time()}\n")
                            with open("userChannel.txt", "a") as file:
                                file.write(f"{payload.user_id},{text_channel.id}\n")
                        except Exception as e:
                            print("Error writing to file:", e)

                if payload.emoji.name == "🫂":
                    query = """
                        INSERT INTO reputation (userID, rep)
                        VALUES ($1, $2)
                        ON CONFLICT (userID)
                        DO UPDATE SET rep = (reputation.rep + 1);
                    """
                    await self.conn.execute(query, payload.member.id, 1)

                if payload.emoji.name == "🗣️":
                    query = """
                        INSERT INTO reputation (userID, rep)
                        VALUES ($1, $2)
                        ON CONFLICT (userID)
                        DO UPDATE SET rep = (reputation.rep + 1);
                    """
                    await self.conn.execute(query, payload.member.id, 1)

                if payload.emoji.name == "⬆️":
                    query = """
                        INSERT INTO reputation (userID, rep)
                        VALUES ($1, $2)
                        ON CONFLICT (userID)
                        DO UPDATE SET rep = (reputation.rep + 1);
                    """
                    await self.conn.execute(query, payload.member.id, 1)

                if payload.emoji.name == "🔍":
                    channel = self.bot.get_channel(payload.channel_id)
                    message = channel.get_partial_message(payload.message_id)
                    await message.remove_reaction(payload.emoji ,payload.member)
                    em = discord.Embed(
                        description="No one can access this channel even server owners wont have a look on custom private vent channels because we respect privacy. You are here all by yourself so dont worry about getting judged and feel free to vent.\nWhatever you'll vent about here will be posted publicly on one of the above VENT AREA channels (you can decide when you vent) but no one can know who typed it and what is their identity so feel safe.\n__Once you are done venting out, we will delete this channel to avoid maxing out server channel space.__\n\n**Why keeping us anonymous?**\nWe try our best to help people across the globe to deal with whatever they are going through.\nSince many people on the internet are insecure about getting judged and dealing with toxicity online, we try to minimize it by keeping you anonymous.\n\n**Why are we doing this?**\nWe understand how tough life can get and we understand it can be really difficult for one to go through all the pain and sufferings.\nAll we want is you to move forward in life and this effort is a little push to that. We want to let you know that you are not alone in this game, a lot of people on the world share similar pain. (knowing this definitely helps one to move forward)\n\nSometimes it is better to let your heart cry out loud in a place where no one will judge you, and that is where this server comes in play."
                    )
                    em.set_author(name="Information: ",
                                icon_url="https://99gifshop.neocities.org/items/new/reverseearth.gif")
                    channel = self.bot.get_channel(payload.channel_id)
                    txt = await channel.fetch_message(payload.message_id)
                    await txt.edit(embed=em)
                    await txt.add_reaction('\U00002b05')
                if payload.emoji.name == '\U00002b05':
                    server = self.bot.get_guild(payload.guild_id)
                    channel = server.get_channel(payload.channel_id)
                    message = channel.get_partial_message(payload.message_id)
                    await message.remove_reaction(payload.emoji ,payload.member)
                    ema = discord.Embed(
                        description="1) Make your text fit in one single message because the channel will be deleted once your vent is posted in public channels.\n\n2) Dm <@962603846696337408> to get your message deleted or edited (A staff member will assist you).\n\n3) You can DM <@962603846696337408> bot for any help related to the server.\n\nPlease vent here in this channel and not in bot's DM.\n__React with 🔍 emoji for more information__"
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
                # Define function to create inbox channels
                async def create_inbox_channel(guild, user, msg_owner, inbox_code):
                    try:
                        category = discord.utils.get(guild.categories, name="📨 INBOX")
                        text_channel_replier = await category.create_text_channel(inbox_code)

                        # Set permissions for the user and message owner
                        await text_channel_replier.set_permissions(user, send_messages=True, view_channel=True)
                        await text_channel_replier.set_permissions(msg_owner, view_channel=False)
                        # Explicitly deny @everyone to view the channel
                        await text_channel_replier.set_permissions(guild.default_role, view_channel=False)

                        # Create corresponding channel for message owner
                        text_channel_owner = await category.create_text_channel(inbox_code)
                        await text_channel_owner.set_permissions(user, view_channel=False)
                        await text_channel_owner.set_permissions(msg_owner, send_messages=True, view_channel=True)
                        await text_channel_owner.set_permissions(guild.default_role, view_channel=False)

                        return text_channel_replier, text_channel_owner
                    except Exception as e:
                        print(f"Error creating inbox channels: {e}")

                # Insert reputation and remove reaction
                query = """
                    INSERT INTO reputation (userID, rep)
                    VALUES ($1, $2)
                    ON CONFLICT (userID)
                    DO UPDATE SET rep = (reputation.rep + 1);
                """
                await self.conn.execute(query, payload.member.id, 1)

                channel = self.bot.get_channel(payload.channel_id)
                message = channel.get_partial_message(payload.message_id)
                await message.remove_reaction(payload.emoji, payload.member)

                # Check if message exists in database
                db_data = collection.find_one({"msg_id": payload.message_id})
                if db_data:
                    guild = self.bot.get_guild(payload.guild_id)
                    msg_owner = guild.get_member(int(db_data["author_id"]))

                    if msg_owner:
                        inbox_code = ''.join(choice('1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890') for _ in range(randint(2, 5)))
                        text_channel_replier, text_channel_owner = await create_inbox_channel(guild, payload.member, msg_owner, inbox_code)

                        # Send instructions and message to inbox owner
                        ventMsg = discord.Embed(description=f"{db_data['msg_link']}")
                        ventMsg.set_author(name="Anonymous", icon_url="https://res.cloudinary.com/teepublic/image/private/s--UymRXkch--/t_Resized%20Artwork/c_fit,g_north_west,h_1054,w_1054/co_ffffff,e_outline:53/co_ffffff,e_outline:inner_fill:53/co_bbbbbb,e_outline:3:1000/c_mpad,g_center,h_1260,w_1260/b_rgb:eeeeee/c_limit,f_auto,h_630,q_90,w_630/v1570281377/production/designs/6215195_0.jpg")
                        await text_channel_owner.send(f"Someone wants to talk to you about your vent. You'll receive their message here and you can reply to it by texting here. <@{db_data['author_id']}>", embed=ventMsg)

                        # Inserting inbox information in the database
                        post = {"channel": f"{inbox_code}", "reactor": payload.member.id, "author": int(db_data["author_id"])}
                        inbox.insert_one(post)
                    else:
                        await payload.member.send("Vent message owner not found! They probably left the server.")
                else:
                    print('Cannot find message id in database!')
                    await payload.member.send('Vent author left the server!')
        except Exception as err:
            print(err)

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
            if reaction.emoji == "\U0001f48c": 
                await wokchn()
                cofirm = await reaction.message.channel.send("`📩` - Accept Private Anonymous Message\n`☘️` - Do not accept private anonymous message\n\n**Note:** Person who will send private message to you wont be able to know who you are and you wont be able to know who they are.")
                await cofirm.add_reaction("📩")
                await cofirm.add_reaction("☘️")
                await reaction.message.delete()
        if not user.bot:
            if reaction.emoji == "📩":
                try:
                    await accept()
                    await reaction.message.delete()
                except Exception as e: 
                    print(e)
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
                try:
                    channel = discord.utils.get(guild.channels, name=f'{before.name}s-vent-{before.discriminator}')
                    await channel.edit(name=f'{after.name}s-vent-{after.discriminator}')
                except: 
                    channel = discord.utils.get(guild.channels, name=f'{before.name}s-vent')
                    await channel.edit(name=f'{after.name}s-vent-{after.discriminator}')
            except Exception as err: 
                logchannel = self.bot.get_channel(1089639606091259994)
                await logchannel.send(f"<:disagree:943603027854626816> Failed to change {after.name}#{after.discriminator}'s channel name because __`before.name` did not match `after.name`__\
                \n```{traceback.format_exc()}```")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.guild.id == 943556434644328498:
            guild = self.bot.get_guild(943556434644328498)
            leaveChannel = self.bot.get_channel(1089639606091259994)
            em = discord.Embed(description=f"<:disagree:943603027854626816> {member.name} ({member.id}) left!", colour=discord.Colour.red())
            x = await leaveChannel.send(embed=em)

            # Getting uniqueUserId 
            if ventUserId.find_one({"user": member.id}):
                data = ventUserId.find_one({"user": member.id})
                uId = data["uniqueId"]
    
            # Read the userChannel.txt file
            with open("userChannel.txt", "r") as user_file:
                user_lines = user_file.readlines()

            # Check if the user ID is stored in the file
            user_id_to_remove = str(member.id)
            updated_user_lines = []
            channel_id_to_remove = None
            for user_line in user_lines:
                user_id, channel_id = user_line.strip().split(",")
                if user_id != user_id_to_remove:
                    updated_user_lines.append(user_line)
                else:
                    channel_id_to_remove = channel_id

            # Write the updated user lines back to the file
            with open("userChannel.txt", "w") as user_file:
                user_file.writelines(updated_user_lines)

            # Delete the associated text channel
            if channel_id_to_remove:
                try:
                    channel_to_delete = guild.get_channel(int(channel_id_to_remove))
                    await channel_to_delete.delete()
                    await leaveChannel.send(f"Text channel {channel_to_delete.name} ({channel_id_to_remove}) deleted.")
                except Exception as e:
                    await leaveChannel.send(f"Error deleting channel: {e}")
            else:
                await leaveChannel.send(f"No associated channel found for user {member.name} ({member.id}).")

            # Removing reputation
            try: 
                query = """
                    DELETE FROM reputation
                    WHERE userid = $1;
                """
                await self.conn.execute(query, member.id)
                await leaveChannel.send("Reputation data removed from DB!")
            except Exception as e:
                await leaveChannel.send(f"Faced issue while deleting rep data: {e}")

            try: 
                collection.delete_many({'author_id': member.id})
                prof.delete_one({"user": member.id})
                if ventUserId.find_one({'user': member.id}): 
                    ventUserId.delete_one({'user': member.id})
            except:
                pass

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 943556434644328498:
            joinChannel = self.bot.get_channel(1089639606091259994)
            em = discord.Embed(description=f"<:agree:943603027313565757> {member.name} ({member.id}) joined!", colour=discord.Colour.green())
            x = await joinChannel.send(embed=em)  

            # Check if member's name contains all three strings "evil", "like", and "you" (in any order)
            name = member.name.lower()
            if "evil" in name and "like" in name and "you" in name:
                await member.ban(reason="Vegan troller suspected")
                await joinChannel.send(f"Banned {member.name} ({member.id}) - Vegan troller suspected!!")
                return  # Don't execute the rest of the function if the member is banned

            try: 
                query = """
                    INSERT INTO reputation (userID, rep)
                    SELECT $1, $2
                    WHERE NOT EXISTS (
                        SELECT 1 FROM reputation WHERE userID = $1
                    );
                """
                await self.conn.execute(query, member.id, 0)
            except Exception as e:
                print(e)

            start_time = time.time()
            if member.guild.id == 943556434644328498:
                # Storing unqiue user id
                if not ventUserId.find_one({"user": member.id}):
                    characters = '1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
                    uniqueId = "".join(choice(characters)
                                    for x in range(randint(20, 25)))
                    userSavePost = {"user": member.id, "uniqueId": uniqueId}
                    ventUserId.insert_one(userSavePost)
                else: 
                    pass
            end_time = time.time()
            elapsed_time = end_time - start_time
            await joinChannel.send(f"`Elapsed time: {elapsed_time:.2f}s`")  
            await x.add_reaction('\U00002714')

            # if channels are exceeding 
            if len(member.guild.text_channels) == 500: 
                await joinChannel.send(f'\U000026a0 <@{943928873412870154}><@{852797584812670996} server channel limit exceeding!')

async def setup(bot):
    await bot.add_cog(_events(bot))
