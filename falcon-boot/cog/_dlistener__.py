from discord.ext import commands
from discord import utils
import discord
import asyncio
from random import *
from pymongo import MongoClient, message

# gChat, dUser, dHistory, collection 
class dlistener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    global db, gChat, dUser, dHistory, collection, inbox
    cluster = MongoClient(
        "mongodb+srv://Edryu:jaisairam4@cluster0.inbe1.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = cluster["Dating"]
    collection = db["DatingProfile"]
    gChat = db['DatingGlobal']
    dHistory = db['DatingHistory']
    dUser = db['DatingUser']
    inbox = db['DatingInbox']

    global repButton
    class repButton(discord.ui.View):
        def __init__(self, *, timeout=3600):
            super().__init__(timeout=timeout)
        @discord.ui.button(label="Report User",style=discord.ButtonStyle.danger, disabled=False)
        async def gray_button(self, interaction:discord.Interaction, button:discord.ui.Button):
            button.disabled=True
            button.label="Reported"
            button.style=discord.ButtonStyle.gray
            await interaction.response.edit_message(view=self)

            data = inbox.find_one({"reactor":interaction.user.id})
            channel = interaction.client.get_channel(1000432578320400404)
            if inbox.find_one({"reactor":interaction.user.id}):
                author = interaction.client.get_user(int(data['author']))

                interChn = interaction.client.get_channel(interaction.channel_id)
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

                #Blocking users
                repoterUser = interaction.client.get_user(data['reactor'])
                await interaction.channel.set_permissions(repoterUser, send_messages=False, view_channel=True)
                reportedUser = interaction.client.get_user(data['author'])
                await chn.set_permissions(reportedUser, send_messages=False, view_channel=True)
            elif inbox.find_one({"author":interaction.user.id}):
                data = inbox.find_one({"author":interaction.user.id})
                reactor = interaction.client.get_user(int(data['reactor']))

                interChn = interaction.client.get_channel(interaction.channel_id)
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

                #Blocking users
                repoterUser = interaction.client.get_user(data['author'])
                await interaction.channel.set_permissions(repoterUser, send_messages=False, view_channel=True)
                reportedUser = interaction.client.get_user(data['reactor'])
                await chn.set_permissions(reportedUser, send_messages=False, view_channel=True)
            else: 
                await interaction.channel.send("UhOh! Looks like something went wrong. Please DM me to report the user instead.")


    @commands.Cog.listener()
    async def on_message(self, msg):
        if not msg.guild:
            return
        if msg.guild.id == 999682901308342342:
            if not dUser.find_one({"mem": msg.author.id}):
                if msg.channel.category is not None:
                    if msg.channel.category.id == 1000038353854533773: #is triggered only in inbox channels 
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
                                    x = await chn.send(embed=em, view=repButton())
                                    await msg.add_reaction("<:agree:943603027313565757>")
            
            #Global Chat 
            if not msg.author.bot:
                if not msg.content.startswith("."):
                    if not dUser.find_one({"mem": msg.author.id}):
                        if msg.channel.category.id == 999927005179035738: 
                            if collection.find_one({"_id": msg.author.id}):
                                if gChat.find_one({"_id": msg.author.id}):
                                    data = gChat.find_one({"_id": msg.author.id})
                                    if data['ident'] == 0:
                                        return
                                    else: 
                                        #post1 = {"lastmessage": msg.author.id}
                                        his = dHistory.find_one({"lastmessage": msg.author.id})
                                        globalChannel = msg.guild.get_channel(1000989536861560862)
                                        gender = collection.find_one({"_id": msg.author.id})
                                        try: 
                                            if not his['lastmessage'] == msg.author.id:
                                                print("if block")
                                                if gender["gender"].lower() == "male":
                                                    col = 0x8ED1FC
                                                elif gender["gender"].lower() == "female":
                                                    col = 0xF78DA7
                                                else: 
                                                    value = random.randint(0, 0xffffff)
                                                    col = value

                                                emd = discord.Embed(description=f"[**{data['username']}**] {msg.content}", color=col)
                                                x = await globalChannel.send(embed=emd) 
                                                dHistory.delete_many({})
                                                post1 = {"lastmessage": msg.author.id, "msg_id": x.id , "text":msg.content}
                                                # post2 = {"msgby": msg.author.id, "text": msg.content}
                                                dHistory.insert_one(post1)
                                                return
                                                #dHistory.insert_one(post2) 
                                                #await globalChannel.send(f'{data["username"]}```{msg.content}```')
                                            else: 
                                                print("else block")
                                                if gender["gender"].lower() == "male":
                                                    col = 0x8ED1FC
                                                elif gender["gender"].lower() == "female":
                                                    col = 0xF78DA7
                                                else: 
                                                    value = random.randint(0, 0xffffff)
                                                    col = value
                                                
                                                oldtext = dHistory.find_one({"lastmessage": msg.author.id})
                                                emd = discord.Embed(description=f"[**{data['username']}**] {str(oldtext['text'])}\n    {msg.content}", color=col)
                                                #await globalChannel.send(embed=emd) 
                                                txt = await globalChannel.fetch_message(int(oldtext["msg_id"]))
                                                x = await txt.edit(embed=emd)
                                                #await globalChannel.send(f"```{msg.content}```")
                                                # print('1')
                                                dHistory.delete_many({})
                                                # print('2')
                                                post1 = {"lastmessage": msg.author.id, "msg_id": x.id , "text":f"{oldtext['text']}\n   {msg.content}"}
                                                # print('3')
                                                dHistory.insert_one(post1)
                                                # print('4 (sucess)')
                                                return
                                                #dHistory.delete_many({})
                                        except: 
                                                print("except block")
                                                if gender["gender"].lower() == "male":
                                                    col = 0x8ED1FC
                                                elif gender["gender"].lower() == "female":
                                                    col = 0xF78DA7
                                                else: 
                                                    value = random.randint(0, 0xffffff)
                                                    col = value
                                                emd = discord.Embed(description=f"[**{data['username']}**] {msg.content}", color=col)
                                                x = await globalChannel.send(embed=emd) 
                                                #await globalChannel.send(f'{data["username"]}```{msg.content}```')
                                                dHistory.delete_many({})
                                                post1 = {"lastmessage": msg.author.id, "msg_id": x.id, "text": msg.content}
                                                #post2 = {"msgby": msg.author.id, "text": msg.content}
                                                dHistory.insert_one(post1)
                                                return
                                                #dHistory.insert_one(post2)
                                        

                                else:
                                    post = {"_id": msg.author.id, 'username': "-", 'ident': 0}
                                    gChat.insert_one(post)
                                    await msg.channel.send(f"What will be your `display name`?")

                                    def check(msg):
                                        return msg.author == msg.author and msg.channel == msg.channel and msg.guild.id == 999682901308342342

                                    try:
                                        msg1 = await self.bot.wait_for("message", check=check, timeout=300)
                                    except asyncio.TimeoutError:
                                        error5 = await msg.channel.send(f"<:disagree:943603027854626816> TimedOut {msg.author.mention}")
                                        await asyncio.sleep(5)
                                        await error5.delete()
                                        return
                                    pass
                                    if msg1: 
                                        gChat.update_one({"_id":msg.author.id}, {"$set":{"username":msg1.content}})
                                        gChat.update_one({"_id": msg.author.id}, {"$inc": {"ident": 1}})
                                        await msg.channel.send('Now you can start chatting :)')
                await self.bot.process_commands(msg)
async def setup(bot):
    await bot.add_cog(dlistener(bot))
