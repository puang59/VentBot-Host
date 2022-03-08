from cgitb import text
from pydoc import describe
from discord.ext import commands
import discord
import asyncio
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
    await bot.user.edit(avatar=pfp)


@bot.event
async def status_task():
    while True:
        await bot.change_presence(status=discord.Status.online, activity=discord.Game('Stay strong'))
        await asyncio.sleep(5)
        await bot.change_presence(status=discord.Status.online, activity=discord.Game('DM me for help'))
        await asyncio.sleep(5)


@bot.event
async def on_ready():
    print("The bot is online!")
    # bot.loop.create_task(pfp())
    bot.load_extension("cogs.onMessage")
    bot.loop.create_task(status_task())


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
            text_channel = await categ.create_text_channel(f"{member.name}s vent")
            await text_channel.set_permissions(user_a, send_messages=True, view_channel=True)
            await text_channel.set_permissions(guild.default_role, send_messages=False, view_channel=False)
            await text_channel.set_permissions(role_b, send_messages=False)
            await text_channel.edit(topic=f"Custom PRIVATE Vent channel for {member.name}")
            await text_channel.edit(slowmode_delay=7200)

            em = discord.Embed(
                description="**Before you proceed:**\nNo one can access this channel even server owners wont have a look on custom private vent channels because we respect privacy. You are here all by yourself so dont worry about getting judged and feel free to vent.\nWhatever you'll vent about here will be posted publicly on <#943556439195152477> channel but no one can know who typed it and what is their identity so feel safe.\n__Once you are done venting out, we will temporarily BLOCK you from sending any message here to avoid spams and trolls.__\n\n**Why keeping us anonymous?**\nWe try our best to help people across the globe to deal with whatever they are going through.\nSince many people on the internet are insecure about getting judged and dealing with toxicity online, we try to minimize it by keeping you anonymous.\n\n**Why are we doing this?**\nWe understand how tough life can get and we understand it can be really difficult for one to go through all the pain and sufferings.\nAll we want is you to move forward in life and this effort is a little push to that. We want to let you know that you are not alone in this game, a lot of people on the world share similar pain. (knowing this definitely helps one to move forward)\n\nSometimes it is better to let your heart cry out loud in a place where no one will judge you, and that is where this server comes in play."
            )
            em.set_author(name="Please read before TYPING anything: ",
                          icon_url="https://cdn.discordapp.com/attachments/915896229697826829/943564751823306892/images.png")
            ema = discord.Embed(
                description="1) __The bot will temporarily BLOCK you from sending message once you send ONE message here.__ So make your text fit in one single message.\n\n2) If you want to edit or delete your message that was posted in <#943556439195152477>, then you'll have to DM <@943557720273989652> bot mentioning why you want to edit/delete it and a staff member will take care of that.\n **Note:** You'll be completely anonymous to that staff member. They'll ask you for the __message code__ so that they can delete the message directly without having any knowledge of you. Message code will be provided to you once you vent.\n\n3) The bot will unblock you in `2 Hours`, so you can vent again if you want to. (If you arent unblocked, then you can DM <@943557720273989652> bot)\n\nPlease take care of yourself :)"
            )
            ema.set_author(name="Instruction: ",
                           icon_url="https://cdn.discordapp.com/attachments/915896229697826829/943564751823306892/images.png")
            ema.set_footer(
                text="Note: We dont save your details and message in any separate database.")
            await text_channel.send(f"{member.mention}")
            await text_channel.send(embed=em)
            await text_channel.send(embed=ema)


@bot.event
async def on_message(msg):
    if not msg.author.bot:
        if not msg.author.id == 943928873412870154:
            if msg.channel.id != 943556439195152477:
                if not isinstance(msg.channel, discord.channel.DMChannel):
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
                            await member.add_roles(role)

                        #vent_channel = bot.get_channel(f"{member.name}s vent")
                        vent_channel = bot.get_channel(943556439195152477)
                        if msg.author.id == 852797584812670996:
                            pass
                        else:
                            await msg.channel.set_permissions(member, send_messages=False, view_channel=True)
                        em = discord.Embed(
                            description=msg.content
                        )
                        em.set_author(name="Anonymous", icon_url="https://res.cloudinary.com/teepublic/image/private/s--UymRXkch--/t_Resized%20Artwork/c_fit,g_north_west,h_1054,w_1054/co_ffffff,e_outline:53/co_ffffff,e_outline:inner_fill:53/co_bbbbbb,e_outline:3:1000/c_mpad,g_center,h_1260,w_1260/b_rgb:eeeeee/c_limit,f_auto,h_630,q_90,w_630/v1570281377/production/designs/6215195_0.jpg")

                        post = {"author_id": msg.author.id, "code": f"{msg_code}",
                                "msg_link": "no", "msg_id": "no", "channel_id": msg.channel.id, "owner_name": f"{msg.author.name}#{msg.author.discriminator}", "ident": "vent"}
                        collection.insert_one(post)

                        cofirm = await msg.channel.send("Click on `Envelope` reaction to accept private messages on this vent. (Click on `X` if you dont want to accept private message on this vent)\n**Note:** Person who will send private message to you wont be able to know who you are and you wont be able to know who they are.")
                        await cofirm.add_reaction("📩")
                        await cofirm.add_reaction("❌")

                        await bot.wait_for('reaction_add', check=lambda reaction, user: reaction.emoji == '📩')
                        x = await vent_channel.send(embed=em)
                        await x.add_reaction('🫂')
                        await x.add_reaction('💬')
                        collection.update_one({"msg_link": "no"}, {
                                              "$set": {"msg_link": f"{x.jump_url}"}})
                        collection.update_one(
                            {"msg_id": "no"}, {"$set": {"msg_id": x.id}})
                        await cofirm.delete()
                        await msg.reply(f"<:agree:943603027313565757> ||{msg_code}|| - is your message code. __Keep it safe somewhere and dont share.__")

                        await bot.wait_for('reaction_add', check=lambda reaction, user: reaction.emoji == '❌')
                        x = await vent_channel.send(embed=em)
                        await x.add_reaction('🫂')
                        collection.update_one({"msg_link": "no"}, {
                                              "$set": {"msg_link": f"{x.jump_url}"}})
                        collection.update_one(
                            {"msg_id": "no"}, {"$set": {"msg_id": x.id}})
                        await cofirm.delete()
                        await msg.reply(f"<:agree:943603027313565757> ||{msg_code}|| - is your message code. __Keep it safe somewhere and dont share.__")

                        try:
                            data = collection.find_one({"code": msg_code})
                            link = data["msg_link"]
                            emdm = discord.Embed(
                                description=f"||{msg_code}|| - {link}")
                            await msg.author.send("<:agree:943603027313565757> Things went right! Stay strong, we believe in you. ᕦ(ò_óˇ)ᕤ", embed=emdm)
                        except:
                            print("DMs closed")

                        await asyncio.sleep(7200)
                        await member.remove_roles(role)
                        await msg.channel.set_permissions(member, send_messages=True, view_channel=True)
    await bot.process_commands(msg)


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
    role = discord.utils.get(ctx.guild.roles, name="Blocked")
    await member.remove_roles(role)
    await ch.set_permissions(member, send_messages=True, view_channel=True)

    # deleting message from vent channel
    channel = bot.get_channel(943556439195152477)
    txt = await channel.fetch_message(data["msg_id"])
    await txt.delete()
    collection.delete_one({"code": code})

    await ctx.send("<:agree:943603027313565757> Edit opened successfully")


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
    '''
    Channel = bot.get_channel('')
    if reaction.message.channel.id != Channel
    return
    '''
    if not user.bot:
        if reaction.emoji == "💬":
            if collection.find_one({"msg_id": reaction.message.id}):
                db_data = collection.find_one({"msg_id": reaction.message.id})
                guild = user.guild
                user_a = user
                role_b = discord.utils.get(user.guild.roles, name="Blocked")
                server = bot.get_guild(943556434644328498)
                msg_owner = server.get_member(db_data["owner_name"])

                #print(f"msg_owner: {msg_owner}")
                #print(f"user_a: {user_a}")

                categ = discord.utils.get(guild.categories, name="INBOX")
                text_channel = await categ.create_text_channel(f"{user.discriminator}")
                await text_channel.set_permissions(user_a, send_messages=True, view_channel=True)
                await text_channel.set_permissions(guild.default_role, send_messages=False, view_channel=False)
                await text_channel.set_permissions(role_b, send_messages=False)
                await text_channel.set_permissions(msg_owner, send_messages=True, view_channel=True)
                await text_channel.edit(topic=f"Anonymous PRIVATE Message on {db_data['msg_link']}")
            else:
                print('Cannot find message id in DataBase!')

    '''
    if reaction.emoji == "📩":
        #reactor = 123
        async for user in reaction.users():
            
            if user.bot:
                pass
            else:
                reactor += user.id
                print(reactor)
            
            if collection.find_one({"author_id": user.id}):
                print("worked")
                db_data = collection.find_one({"author_id": user.id})
                textem = db_data['msg_id']
                await textem.add_reaction("💬")
            else:
                print("0worked")
                return
    '''
# token removed
# bot.run("OTQ5ODUyMDM3MzIxOTkwMTY2.YiQYpQ.24uOmgwVCWjs5Z4lYzx5Rk3Z4ac")
