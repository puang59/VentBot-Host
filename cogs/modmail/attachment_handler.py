# \U00002705 -> checkmark emoji

import discord
from random import randint

async def successMessage(message: discord.Message) -> None:
    dmEmbed = discord.Embed(
        description="Your message is successfully sent to staff team. They'll respond as soon as possible.",
        color=discord.Colour.green()
    )
    dmEmbed.set_author(
        name="Message Sent", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/Sign-check-icon.png/640px-Sign-check-icon.png")
    await message.author.send(embed=dmEmbed, delete_after=10)

# handling messages with attachments
async def ifattachments(message: discord.Message, categ: discord.CategoryChannel, mod_role: discord.Role) -> None:
    link = [attachment.url for attachment in message.attachments]
    channel = discord.utils.get(categ.channels, topic=str(message.author.id))

    if not channel:  
        channel = await categ.create_text_channel(name=f"{randint(1000000000, 9999999999)}", topic=str(message.author.id))
        await channel.send(f"New Mail | {mod_role.mention}")
        await successMessage(message)

    # if there is only one attachment and message is not empty then send an embed with image and message
    if len(link) == 1 and message.content != "":
        embed = discord.Embed(description=message.content, colour=0x696969)
        embed.set_image(url=f"{link[0]}")
        embed.set_author(name="Anonymous", icon_url="https://shorturl.at/ceAP3")

        await channel.send(embed=embed)
        await message.add_reaction("\U00002705")

        return 

    # if message content is not empty then send an embed with message 
    if not message.content == "":
        embed = discord.Embed(description=message.content, colour=0x696969) # haha funny number
        embed.set_author(name="Anonymous", icon_url="https://shorturl.at/ceAP3")
        await channel.send(embed=embed)

    # send all the attachments in a loop and each in different embeds 
    for url in link: 
        image_embed = discord.Embed(colour=0x696969)
        image_embed.set_image(url=f"{url}")
        await channel.send(embed=image_embed)

    await message.add_reaction("\U00002705")

# handling messages without attachments
async def ifnotattachments(message: discord.Message, categ: discord.CategoryChannel, mod_role: discord.Role) -> None: 
    channel = discord.utils.get(categ.channels, topic=str(message.author.id))

    if not channel:
        channel = await categ.create_text_channel(name=f"{randint(1000000000, 9999999999)}", topic=str(message.author.id))
        await channel.send(f"New Mail | {mod_role.mention}")
        await successMessage(message)

    embed = discord.Embed(description=message.content, colour=0x696969)
    embed.set_author(name="Anonymous", icon_url="https://shorturl.at/ceAP3")
    
    await channel.send(embed=embed)

    await message.add_reaction("\U00002705")
