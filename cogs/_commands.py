from discord.ext import commands
import discord
import asyncio

import config

class _commands(commands.Cog):
    """General server commands"""
    def __init__(self, bot):
        self.bot = bot
        self.conn = None

    async def cog_load(self):
        self.conn = await self.bot.get_db_connection()

    @commands.command(aliases=["rep"])
    # @commands.check(lambda ctx: ctx.author.id in config.admins)
    async def reputation(self, ctx, member: discord.Member = None):
        """Shows reputation earned by the specificed user"""
        if member is None:
            member = ctx.author

        await ctx.send("This command is temporarily disabled!")

    @commands.command(aliases=["rep"])
    # @commands.check(lambda ctx: ctx.author.id in config.admins)
    async def reputation(self, ctx, member: discord.Member = None):
        """Shows reputation earned by the specificed user"""
        if member is None:
            member = ctx.author

        confirmation = await ctx.send("Fetching...")
        query = "SELECT * FROM reputation WHERE userID = $1;"
        data = await self.conn.fetchrow(query, member.id)
        if data:
            rep = data['rep']
            embed = discord.Embed(
                description=f"Server Reputation:```{rep} rep```", colour=discord.Colour.lighter_grey())
            embed.set_author(name=member.name, icon_url=member.avatar.url if member.avatar else None)

            await confirmation.delete()
            await ctx.send(embed=embed)
        else:
            insert_query = "INSERT INTO reputation (userID, rep) VALUES ($1, $2)"
            await self.conn.execute(insert_query, member.id, 0)
            await confirmation.delete()
            await ctx.send("You don't have any server activity as of now.")

    @commands.command()
    async def setrep(self, ctx, member: discord.Member, rep: int):
        """Modifies reputation points of mentioned user"""
        confirmation = await ctx.send("Updating...")
        query = """
            SELECT * FROM reputation
            WHERE userId = $1;
        """
        data = await self.conn.fetchrow(query, member.id)
        if data:
            update_query = """
                UPDATE reputation
                SET rep = $1
                WHERE userID = $2;
            """
            await self.conn.execute(update_query, rep, member.id)
            await confirmation.delete()
            await ctx.send("Updated data")
        else:
            await confirmation.delete()
            await ctx.send("User does not exist!")

    @commands.command()
    async def lb(self, ctx):
        """Shows reputation leaderboard"""
        query = "SELECT * FROM reputation ORDER BY rep DESC LIMIT 20;"
        results = await self.conn.fetch(query)

        temp = ""
        i = 1
        guild = self.bot.get_guild(943556434644328498)

        for result in results:
            member = guild.get_member(result['userid'])
            if not member:
                continue

            if i <= 3:
                place = ["🥇", "🥈", "🥉"][i-1]
            else:
                place = f"<:blank:988101402314297384>"

            embed_show = f"{place} `{result['rep']:,} rep` - {member.name}\n"
            temp += embed_show

            i += 1

        if temp:
            embed = discord.Embed(description=f"{temp}")
            embed.colour = 0x2e3137
            embed.set_author(
                name="Reputation Leaderboard",
                icon_url=guild.icon.url
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(_commands(bot))
