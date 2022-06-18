from cgitb import text
from pydoc import describe
from discord.ext import commands, tasks
import aiohttp
import discord
import asyncio
import os
from random import *

from pymongo import MongoClient

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix=".", intents=intents)
bot.remove_command("help")

global cluster
global db
global collection
cluster = MongoClient(
    "mongodb+srv://Edryu:jaisairam4@cluster0.inbe1.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["Discord"]
collection = db["vent"]

async def pfp():
    pfp = open(f"image.png", "rb").read()

@bot.event
async def status_task():
    while True:
        await bot.change_presence(status=discord.Status.online, activity=discord.Game('Stay strong'))
        await asyncio.sleep(5)
        await bot.change_presence(status=discord.Status.online, activity=discord.Game('DM me for help'))
        await asyncio.sleep(5)


async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load_cogs()
        print("Cogs Loadd\nBot ready!")
        await bot.start('OTYyNjAzODQ2Njk2MzM3NDA4.GazOQC.P1jXz9ZcqnT6ZAbnpE9NNJVVd5M53K-04VDHTs')

@bot.event
async def on_member_join(member):
    if member.guild.id == 943556434644328498:
        if collection.find_one({"author_id": member.id}):
            data = collection.find_one({"author_id": member.id})
            ch = bot.get_channel(int(data["channel_id"]))
            await ch.set_permissions(member, send_messages=True, view_channel=True)
        else:
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

@bot.event
async def on_member_remove(member):
    guild = bot.get_guild(943556434644328498)
    try: 
        channel = discord.utils.get(guild.channels, name=f'{member.name}s-vent-{member.discriminator}')
        await channel.delete()
    except: 
        channel = discord.utils.get(guild.channels, name=f'{member.name}s-vent')
        await channel.delete()

@bot.event
async def on_message(msg):
    if not msg.author.bot:
        if not msg.author.id == 943928873412870154:
            if not msg.author.id == 852797584812670996:
                if msg.channel.id != 943556439195152477:
                    if not isinstance(msg.channel, discord.channel.DMChannel):
                        if not msg.channel.category.id == 950646823654137897:
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
                                    # if msg.author.id == 852797584812670996:
                                    #     pass
                                    # else:
                                    #     await msg.channel.set_permissions(member, send_messages=False, view_channel=True)
                                    em = discord.Embed(
                                        description=msg.content
                                    )

                                    cofirm = await msg.channel.send("Click on `Envelope` reaction to accept private messages on this vent. (Click on `X` if you dont want to accept private message on this vent)\n**Note:** Person who will send private message to you wont be able to know who you are and you wont be able to know who they are.")
                                    await cofirm.add_reaction("📩")
                                    await cofirm.add_reaction("❌")

                                    global cross

                                    async def cross():
                                        em.set_author(name="Anonymous", icon_url="https://res.cloudinary.com/teepublic/image/private/s--UymRXkch--/t_Resized%20Artwork/c_fit,g_north_west,h_1054,w_1054/co_ffffff,e_outline:53/co_ffffff,e_outline:inner_fill:53/co_bbbbbb,e_outline:3:1000/c_mpad,g_center,h_1260,w_1260/b_rgb:eeeeee/c_limit,f_auto,h_630,q_90,w_630/v1570281377/production/designs/6215195_0.jpg")
                                        x = await vent_channel.send(embed=em)
                                        await x.add_reaction('🫂')
                                        post = {"author_id": msg.author.id, "code": f"{msg_code}",
                                                "msg_link": f"{x.jump_url}", "msg_id": x.id, "channel_id": msg.channel.id, "owner_name": f"{msg.author.name}#{msg.author.discriminator}", "ident": "vent"}
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
                                            await msg.author.send("<:agree:943603027313565757> Things went right! Stay strong, we believe in you. ᕦ(ò_óˇ)ᕤ", embed=emdm)
                                        except:
                                            print("DMs closed")

                                        # await asyncio.sleep(7200)
                                        # await member.remove_roles(role)
                                        # await msg.channel.set_permissions(member, send_messages=True, view_channel=True)

                                    global accept

                                    async def accept():
                                        em.set_author(name="Anonymous", icon_url="https://res.cloudinary.com/teepublic/image/private/s--UymRXkch--/t_Resized%20Artwork/c_fit,g_north_west,h_1054,w_1054/co_ffffff,e_outline:53/co_ffffff,e_outline:inner_fill:53/co_bbbbbb,e_outline:3:1000/c_mpad,g_center,h_1260,w_1260/b_rgb:eeeeee/c_limit,f_auto,h_630,q_90,w_630/v1570281377/production/designs/6215195_0.jpg")
                                        em.set_footer(
                                            text="You can click on speech-bubble emoji to reply to this vent and talk to the author anonymously.", icon_url="https://kidsattennis.ca/wp-content/uploads/2020/05/greenball.png")
                                        x = await vent_channel.send(embed=em)
                                        await x.add_reaction('🫂')
                                        await x.add_reaction('💬')
                                        post = {"author_id": msg.author.id, "code": f"{msg_code}",
                                                "msg_link": f"{x.jump_url}", "msg_id": x.id, "channel_id": msg.channel.id, "owner_name": f"{msg.author.name}#{msg.author.discriminator}", "ident": "vent"}
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
                                            await msg.author.send("<:agree:943603027313565757> Things went right! Stay strong, we believe in you. ᕦ(ò_óˇ)ᕤ", embed=emdm)
                                        except:
                                            print("DMs closed")

            # Inbox
            if isinstance(msg.channel, discord.TextChannel):
                if msg.channel.category is not None:
                    if msg.channel.category.id == 950646823654137897:
                        if not msg.author.bot:
                            if msg.content.startswith("."):
                                pass
                            else:
                                topic = msg.channel.topic
                                chn = msg.guild.get_channel(int(topic))
                                em = discord.Embed(
                                    description=msg.content
                                )
                                em.set_author(
                                    name="Stranger", icon_url="https://image.similarpng.com/very-thumbnail/2020/08/Emoji-social-media-Reaction-heart-icon-vector-PNG.png")
                                await chn.send(embed=em)
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
    if ctx.channel.category.name == "📨 INBOX":
        topic = ctx.channel.topic
        guild = bot.get_guild(943556434644328498)
        other_chn = guild.get_channel(int(topic))
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
    txt = await channel.fetch_message(data["msg_id"])
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
async def dm(ctx, *, message):
    for user in ctx.guild.members:
        try:
            await user.send(message)
            print(f"Sent {user.name} a DM.")
        except:
            print(f"Couldn't DM {user.name}.")
    print("Sent all the server a DM.")


@bot.event
async def on_reaction_add(reaction, user):
    if not user.bot:
        if reaction.emoji == "📩":
            await accept()

    if not user.bot:
        if reaction.emoji == "❌":
            await cross()

@bot.event
async def on_raw_reaction_add(payload):
    if not payload.member.bot:
        if payload.emoji.name == "🔍":
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

                    categ = discord.utils.get(guild.categories, name="📨 INBOX")

                    text_channel_replier = await categ.create_text_channel(f"{payload.member.discriminator}")

                    await text_channel_replier.set_permissions(user_a, send_messages=True, view_channel=True)
                    await text_channel_replier.set_permissions(msg_owner, view_channel=False)
                    await text_channel_replier.set_permissions(guild.default_role, send_messages=False, view_channel=False)
                    await text_channel_replier.send(f"You can send your message here and it will be sent to the author automatically! <@{payload.member.id}>\n__(You can use `.bin` command here to close this inbox)__")
                    #collection.update_one({"msg_id": reaction.message.id}, {"$set":{f"inbox{user.discriminator}":text_channel_replier.id}})

                    # await text_channel_replier.set_permissions(role_b, send_messages=False)
                    text_channel_owner = await categ.create_text_channel(f"{payload.member.discriminator}")

                    await text_channel_owner.set_permissions(user_a, view_channel=False)
                    await text_channel_owner.set_permissions(msg_owner, send_messages=True, view_channel=True)
                    await text_channel_owner.set_permissions(guild.default_role, send_messages=False, view_channel=False)
                    await text_channel_owner.edit(topic=f"{str(text_channel_replier.id)}")
                    await text_channel_replier.edit(topic=f"{str(text_channel_owner.id)}")
                    await text_channel_owner.send(f"Someone wants to talk to you about {db_data['msg_link']}. You'll recieve their message here and you can reply to it by texting here. <@{db_data['author_id']}>\n__(You can use `.bin` command here to close this inbox)__")

            else:
                print('Cannot find message id in DataBase!')

asyncio.run(main())
