from discord.ext import commands 
import discord 
import asyncio 

import topgg

class _topgg(commands.Cog): 
    def __init__(self, bot) -> None:
        self.bot = bot
    
     
    # @commands.Cog.listener()
    # async def on_dbl_vote(self, data):
    #     print(data)

    @commands.Cog.listener()
    async def on_autopost_success(self):
        self.bot.topgg_webhook = topgg.WebhookManager(self.bot).dbl_webhook("/dblwebhook", "0Uqi220]uS")
        self.topgg_webhook.run(5000)
        print(await self.topggpy.generate_widget({
            "id": 270904126974590976,
            format: "svg"}))

async def setup(bot): 
    await bot.add_cog(_topgg(bot))