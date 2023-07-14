from discord.ext import commands
import discord

# import logging, coloredlogs
import logging.handlers

import datetime
import time
from pytz import timezone

class _logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ########## LOGGER #########


    # coloredlogs.install()

    # logger = logging.getLogger('discord')
    # logger.setLevel(logging.DEBUG)
    # logging.getLogger('discord.http').setLevel(logging.INFO)

    # handler = logging.handlers.RotatingFileHandler(
    #     filename='discord.log',
    #     encoding='utf-8',
    #     maxBytes=32 * 1024 * 1024,  # 32 MiB
    #     backupCount=5,  # Rotate through 5 files
    # )
    # dt_fmt = '%Y-%m-%d %H:%M:%S'
    # formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    # handler.setFormatter(formatter)
    # # handler.setFormatter(CustomFormatter())
    # logger.addHandler(handler)

    # LOCAL LOGS 
    def logInput(type, data): 
        file = open ("./falcon-boot/ventLog.log", "r")  
        lines = file.readlines()
        file.close()
        if type == "at": 
            curdate = datetime.datetime.now(timezone("Asia/Kolkata"))
            for i in range(len(lines)):
                lines[i] = lines[i].rstrip()
                if "AT" not in lines[i]:
                    continue
                else:
                    newLine = f"    AT: [{curdate.day}/{curdate.month}/{curdate.year}] - [{time.strftime('%I:%M %p')}]"
                    lines[i] = newLine

            with open("ventLog.log", "w") as file:
                for line in lines:
                    file.write(line + "\n")

        elif type == "by": 
            for i in range(len(lines)):
                lines[i] = lines[i].rstrip()
                if "BY" not in lines[i]:
                    continue
                else:
                    newLine = f"    BY: {data}"
                    lines[i] = newLine

            with open("ventLog.log", "w") as file:
                for line in lines:
                    file.write(line + "\n")

        elif type == "type": 
            for i in range(len(lines)):
                lines[i] = lines[i].rstrip()
                if "TYPE" not in lines[i]:
                    continue
                else:
                    newLine = f"    TYPE: {data}"
                    lines[i] = newLine

            with open("ventLog.log", "w") as file:
                for line in lines:
                    file.write(line + "\n")

        elif type == "messageid": 
            for i in range(len(lines)):
                lines[i] = lines[i].rstrip()
                if "MESSAGE_ID" not in lines[i]:
                    continue
                else:
                    newLine = f"    MESSAGE_ID: {data}"
                    lines[i] = newLine

            with open("ventLog.log", "w") as file:
                for line in lines:
                    file.write(line + "\n")

    ############################


async def setup(bot):
    await bot.add_cog(_logger(bot))
