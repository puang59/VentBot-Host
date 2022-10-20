from discord.ext import commands
from discord import utils
import discord
import asyncio


class dmsupport(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return  
        # if message.guild.id == 999682901308342342:
        #     return
            
        if isinstance(message.channel, discord.DMChannel):
            if message.attachments:
                link = message.attachments[0].url
                guild = self.bot.get_guild(943556434644328498)
                categ = utils.get(guild.categories, name="MAILS")
                channel = utils.get(
                    categ.channels, topic=str(message.author.id))

                user_a = "852797584812670996"  # evan id

                if not channel:
                    channel = await categ.create_text_channel(name=f"{message.author.discriminator}", topic=str(message.author.id))

                    # evan permission set
                    await channel.set_permissions(user_a, send_messages=True, view_channel=True)

                    notifyrolesd = discord.utils.get(
                        guild.roles, id=943881256033198130)
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

            else:
                guild = self.bot.get_guild(943556434644328498)
                categ = utils.get(guild.categories, name="MAILS")
                channel = utils.get(
                    categ.channels, topic=str(message.author.id))

                if not channel:
                    channel = await categ.create_text_channel(name=f"{message.author.discriminator}", topic=str(message.author.id))
                    notifyrolesd = discord.utils.get(
                        guild.roles, id=943881256033198130)
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
            
    @commands.command()
    async def cogTest(self, ctx): 
        await ctx.send('Working!')

async def setup(bot):
    await bot.add_cog(dmsupport(bot))
