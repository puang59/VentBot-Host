from discord.ext import commands
import discord

import time

class _autoRole(commands.Cog):
    """Self Roles"""
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()

    @commands.command()
    async def autorole(self, ctx): 
        """Auto Role"""
        em = discord.Embed(title="Hide channels", description="`\U00000030 - Hide Serious-vent`\n`\U00000031 - Hide Casual-vent`\n`\U00000032 - Hide Help-vent`\n----------\n`\U00000033 - Hide Whispers-of-kindness`\n`\U00000034 - Hide Global-chat`", color=0x5865F2)
        em.set_footer(text="More than one role can be choosen")
        x = await ctx.send(embed=em)
        await x.add_reaction('\U0001f1e6')
        await x.add_reaction('\U0001f1e7')
        await x.add_reaction('\U0001f1e8')
        await x.add_reaction('\U0001f1e9')
        await x.add_reaction('\U0001f1ea')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guildId = payload.guild_id
        guild = self.bot.get_guild(guild_id)
        member = guild.get_member(payload.user.id)

        if not payload.member.bot: 
            if payload.emoji.name == '\U00000030': # Serious-vent
                role = guild.get_role(1109394091487285318)
                await member.add_roles(role)

            if payload.emoji.name == '\U00000031': # Casual-vent
                role = guild.get_role(1109394240364105778)
                await member.add_roles(role)

            if payload.emoji.name == '\U00000032': # Help-vent
                role = guild.get_role(1109394295439511593)
                await member.add_roles(role)

            if payload.emoji.name == '\U00000033': # Whispers-of-kindness
                role = guild.get_role(1109394345926340619)
                await member.add_roles(role)

            if payload.emoji.name == '\U00000034': # Global-chat
                role = guild.get_role(1109394399114301531)
                await member.add_roles(role)

async def setup(bot):
    await bot.add_cog(_autoRole(bot))
