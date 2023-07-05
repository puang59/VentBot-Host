from discord.ext import commands
from discord import utils
import discord
import asyncio

from pymongo import MongoClient
from random import *

class dmsupport(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    global ventUserId
    cluster = MongoClient("mongodb+srv://Edryu:jaisairam4@cluster0.inbe1.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = cluster["Discord"]
    collection = db["vent"]

    ventUserId = db['ventId']

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user): 
        if not user.bot: 
            if reaction.emoji == "✅":
                await ifvent()
            elif reaction.emoji == "❌":
                await ifnotvent()

    global unique_id_finder
    def unique_id_finder(discordId):
        try: 
            uniqueId = ventUserId.find_one({'user': discordId})
            formattedId = uniqueId['uniqueId'][0:10]
            return formattedId 
        except:
            randomNum = randint(1000000000, 9999999999)
            return randomNum

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return  
        # if message.guild.id == 999682901308342342:
        #     return

        if isinstance(message.channel, discord.DMChannel):

            uniqueId = unique_id_finder(message.author.id)
            
            guild = self.bot.get_guild(943556434644328498)
            categ = utils.get(guild.categories, name="MAILS")
            channel = utils.get(
                categ.channels, topic=str(message.author.id))


            async def ifattachments():
                link = message.attachments[0].url
                guild = self.bot.get_guild(943556434644328498)
                categ = utils.get(guild.categories, name="MAILS")
                channel = utils.get(
                    categ.channels, topic=str(message.author.id))
                if not channel:
                    channel = await categ.create_text_channel(name=f"{uniqueId}", topic=str(message.author.id))

                    notifyrolesd = discord.utils.get(
                        guild.roles, id=1089638056610500778)
                    await channel.send(f"New Mail sent by Anonymous | {notifyrolesd.mention}")

                embed = discord.Embed(
                    description=message.content, colour=0x696969)
                embed.set_image(url=f"{link}")
                embed.set_author(name="Anonymous", icon_url="https://res.cloudinary.com/teepublic/image/private/s--UymRXkch--/t_Resized%20Artwork/c_fit,g_north_west,h_1054,w_1054/co_ffffff,e_outline:53/co_ffffff,e_outline:inner_fill:53/co_bbbbbb,e_outline:3:1000/c_mpad,g_center,h_1260,w_1260/b_rgb:eeeeee/c_limit,f_auto,h_630,q_90,w_630/v1570281377/production/designs/6215195_0.jpg")
                await channel.send(embed=embed)
                embeddm = discord.Embed(
                    description="Your message is successfully sent to the staff team. They'll respond as soon as possible.",
                    color=discord.Colour.green()
                )
                embeddm.set_footer(
                    text="Note: You are totally anonymous and the staff team has no idea about who you are.")
                embeddm.set_author(
                    name="Message Sent", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/Sign-check-icon.png/640px-Sign-check-icon.png")
                dmmsg = await message.author.send(embed=embeddm)
                await asyncio.sleep(20)
                await dmmsg.delete()

            async def ifnotattachments(): 
                guild = self.bot.get_guild(943556434644328498)
                categ = utils.get(guild.categories, name="MAILS")
                channel = utils.get(
                    categ.channels, topic=str(message.author.id))
                if not channel:
                    channel = await categ.create_text_channel(name=f"{uniqueId}", topic=str(message.author.id))
                    notifyrolesd = discord.utils.get(
                        guild.roles, id=1089638056610500778)
                    await channel.send(f"New Mail sent by Anonymous | {notifyrolesd.mention}")

                embed = discord.Embed(
                    description=message.content, colour=0x696969)
                embed.set_author(name="Anonymous", icon_url="https://res.cloudinary.com/teepublic/image/private/s--UymRXkch--/t_Resized%20Artwork/c_fit,g_north_west,h_1054,w_1054/co_ffffff,e_outline:53/co_ffffff,e_outline:inner_fill:53/co_bbbbbb,e_outline:3:1000/c_mpad,g_center,h_1260,w_1260/b_rgb:eeeeee/c_limit,f_auto,h_630,q_90,w_630/v1570281377/production/designs/6215195_0.jpg")
                await channel.send(embed=embed)
                embeddm = discord.Embed(
                    description="Your message is successfully sent to the staff team. They'll respond as soon as possible.",
                    color=discord.Colour.green()
                )
                embeddm.set_footer(
                    text="Note: You are totally anonymous and the staff team has no idea about who you are.")
                embeddm.set_author(
                    name="Message Sent", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/Sign-check-icon.png/640px-Sign-check-icon.png")
                dmmsg = await message.author.send(embed=embeddm)
                await asyncio.sleep(20)
                await dmmsg.delete()


            if not channel:
                confirmation = await message.author.send("Is this a vent message?")
                await confirmation.add_reaction("✅")
                await confirmation.add_reaction("❌")
            
                global ifvent
                async def ifvent(): 
                    await confirmation.delete()
                    await message.author.send("Please use your private vent channel in the server. Bot DMs are for server related help or for reporting someone.")
                    return 

                global ifnotvent
                async def ifnotvent(): 
                    try: 
                        await confirmation.delete()
                    except: 
                        pass
                    if message.attachments:
                        await ifattachments()
                    else: 
                        await ifnotattachments()
            else: #if channel already exists
                if message.attachments:
                    await ifattachments()
                else: 
                    await ifnotattachments()

        elif isinstance(message.channel, discord.TextChannel):
            try: 
                if message.content.startswith(self.bot.command_prefix):
                    pass
                else:
                    topic = message.channel.topic
                    if topic:
                        member = message.guild.get_member(int(topic))
                        if member:
                            embed = discord.Embed(
                                description=message.content, colour=discord.Colour.blue())
                            embed.set_author(
                                name="Staff Team", icon_url="https://www.pngrepo.com/png/121262/512/police.png")
                            await member.send(embed=embed)
            except: 
                pass 

async def setup(bot):
    await bot.add_cog(dmsupport(bot))
