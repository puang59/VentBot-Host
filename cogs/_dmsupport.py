# \U0000274c -> red cross emoji

from discord.ext import commands
from discord import app_commands
import discord
import asyncio 

from cogs.modmail.attachment_handler import ifattachments, ifnotattachments 

GUILD_ID = 943556434644328498
MOD_ROLE = 1089638056610500778

class dmsupport(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        guild = self.bot.get_guild(GUILD_ID)

        if message.author.bot:
            return  


        if isinstance(message.channel, discord.DMChannel): # if message is sent in bot dms
            categ = discord.utils.get(guild.categories, name="MAILS") # make sure category with name MAILS exists 
            mod_role = guild.get_role(MOD_ROLE)

            if message.attachments: # checking if there are attachments
                await ifattachments(message, categ, mod_role)
            else: 
                await ifnotattachments(message, categ, mod_role)

        # directing mod's text to dm of the user
        elif isinstance(message.channel, discord.TextChannel):
            if message.channel.category_id == 943588904622256168:
                try: 
                    if not message.content.startswith(self.bot.command_prefix):
                        topic = message.channel.topic # channel topic contains user id
                        if topic:
                            member = message.guild.get_member(int(topic)) # getting member object from channel topic
                            if member:
                                if message.attachments: # if mod's message contains attachments
                                    link = message.attachments[0].url
                                    embed = discord.Embed(description=message.content)
                                    embed.set_image(url=f"{link}")
                                    embed.set_author(name=f"Mod Team [{message.author.name}]", icon_url="https://discordtemplates.me/icon.png")
                                    await member.send(embed=embed)
                                else: 
                                    embed = discord.Embed(description=message.content) 
                                    embed.set_author(
                                        name=f"Mod Team [{message.author.name}]", icon_url="https://discordtemplates.me/icon.png")
                                    await member.send(embed=embed)
                except Exception as e: 
                   await message.channel.send(f"\U0000274c Failed to send message due to the following error: ```{e}```")
                
    @app_commands.command(name="close")
    @app_commands.default_permissions(administrator=True)
    async def closeCommand(self, interaction: discord.Interaction) -> None:
        """Terminates the help channel"""

        guild = self.bot.get_guild(GUILD_ID)
        if interaction.channel.category.name == "MAILS":
            topic = interaction.channel.topic
            member = guild.get_member(int(topic))

            await interaction.response.send_message("Deleting the channel in 10 seconds!")
            await asyncio.sleep(10)
            await interaction.channel.delete()

            embedclose = discord.Embed(
                description="This thread is closed now. Thank you very much!",
                colour=discord.Colour.lighter_grey()
            )
            embedclose.set_author(
                name="Issue Resolved", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/Sign-check-icon.png/640px-Sign-check-icon.png")
            await member.send(embed=embedclose)

async def setup(bot):
    await bot.add_cog(dmsupport(bot))
