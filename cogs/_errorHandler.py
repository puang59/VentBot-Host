from discord.ext import commands
import discord

class _errorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ########### Error Handling ##########
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            # Check if the command prefix is "..."
            if ctx.prefix == ".." or ctx.prefix == "..." or ctx.prefix == "....":
                pass
        else:
            em = discord.Embed(description=f"Command: `{ctx.command}`\n```{error}```")
            await ctx.send(embed=em)

        # botlog = bot.get_channel(1039589477187858502)
        # msg = await botlog.fetch_message(1039590988181688380)
        # spmsg = msg.content.split()
        # if "```" in spmsg: 
        #     spmsg.remove("```")
        # output = "".join(spmsg)
        # await msg.edit(content = f"``` {output}\n{error} ```")
        #await botlog.send(error)

        raise error
    #####################################

async def setup(bot):
    await bot.add_cog(_errorHandler(bot))
