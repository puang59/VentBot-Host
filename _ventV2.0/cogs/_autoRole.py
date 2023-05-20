from discord.ext import commands
import discord

class _autoRole(commands.Cog):
    """Self Roles"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def autorole(self, ctx): 
        """Auto Role"""
        em = discord.Embed(title="Hide channels", description="`🇦 - Hide Serious-vent`\n`🇧 - Hide Casual-vent`\n`🇨 - Hide Help-vent`\n----------\n`🇩 - Hide Whispers-of-kindness`\n`🇪 - Hide Global-chat`", color=0x5865F2)
        em.set_footer(text="More than one role can be chosen")
        x = await ctx.send(embed=em)
        await x.add_reaction('🇦')
        await x.add_reaction('🇧')
        await x.add_reaction('🇨')
        await x.add_reaction('🇩')
        await x.add_reaction('🇪')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild_id = payload.guild_id
        guild = self.bot.get_guild(guild_id)
        user = guild.get_member(payload.user_id)

        if not user.bot: 
            if payload.emoji.name == '🇦': # Serious-vent
                role = guild.get_role(1109394091487285318)
                await user.add_roles(role)

            if payload.emoji.name == '🇧': # Casual-vent
                role = guild.get_role(1109394240364105778)
                await user.add_roles(role)

            if payload.emoji.name == '🇨': # Help-vent
                role = guild.get_role(1109394295439511593)
                await user.add_roles(role)

            if payload.emoji.name == '🇩': # Whispers-of-kindness
                role = guild.get_role(1109394345926340619)
                await user.add_roles(role)

            if payload.emoji.name == '🇪': # Global-chat
                role = guild.get_role(1109394399114301531)
                await user.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild_id = payload.guild_id
        guild = self.bot.get_guild(guild_id)
        user = guild.get_member(payload.user_id)

        if not user.bot: 
            if payload.emoji.name == '🇦': # Serious-vent
                role = guild.get_role(1109394091487285318)
                await user.remove_roles(role)

            if payload.emoji.name == '🇧': # Casual-vent
                role = guild.get_role(1109394240364105778)
                await user.remove_roles(role)

            if payload.emoji.name == '🇨': # Help-vent
                role = guild.get_role(1109394295439511593)
                await user.remove_roles(role)

            if payload.emoji.name == '🇩': # Whispers-of-kindness
                role = guild.get_role(1109394345926340619)
                await user.remove_roles(role)

            if payload.emoji.name == '🇪': # Global-chat
                role = guild.get_role(1109394399114301531)
                await user.remove_roles(role)

def setup(bot):
    bot.add_cog(_autoRole(bot))
