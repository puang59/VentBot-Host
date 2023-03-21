from discord.ext import commands
import discord
import asyncio


from pymongo import MongoClient

from datetime import datetime, timedelta

class _inboxProtection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    global inboxDB
    cluster = MongoClient("mongodb+srv://Edryu:jaisairam4@cluster0.inbe1.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = cluster["Discord"]
    
    inboxDB = db['ventInboxProtection']

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload): 
        currentTime = datetime.utcnow()
        if not payload.member.bot: 
            if payload.emoji.name == "💬":
                if inboxDB.find_one({"user": payload.member.id}): # if the user already exist in the database 
                    db_data = inboxDB.find_one({"user": payload.member.id})
                    # Convert the time strings to datetime objects
                    fmt = '%H:%M:%S.%f'
                    dbTime = db_data['time']
                    stripdbTime = datetime.strptime(dbTime, fmt) # converting string time stored in database to datetime object so as to perform opertaions
                    currentStripTime = datetime.strptime(str(datetime.utcnow().time()), fmt) # converting current time to datetime object to equalize the format

                    diff = currentStripTime - stripdbTime # getting the difference between the current time and the db time
                    
                    # below line is for debugging
                    #print(f"currentTime: {currentTime.time()} \n stripdbTime: {stripdbTime} \n diff: {diff}")
                    if db_data['counter'] == 1:   
                        inboxDB.update_one({"user": payload.member.id},\
                                           {"$inc": {"counter": 1}})
                        inboxDB.update_one({'user': payload.member.id}, {"$set": {"time": str(currentTime.time())}})                       
                    if db_data['counter'] == 2:
                        if diff.total_seconds() <= float(30): # total_seconds convert the difference time to float
                            timeoutTime = timedelta(minutes=15)
                            await payload.member.timeout(timeoutTime, reason="Inbox ratelimit hit!")
                            inboxDB.delete_one({"user": payload.member.id})
                            try:
                                await payload.member.send("__**You are being rate limited!**__ \n Wait patiently for your server timeout to expire :)")
                            except: 
                                print(f"'You are being rate limited!' was not sent to {payload.member.name} - {payload.member.id}\
                                but they are timed out successfully!")
                        else:
                            inboxDB.delete_one({"user": payload.member.id})
                             
                else: # if the user is not in the db 
                    post = {"user": payload.member.id, "counter": 1, "time":str(currentTime.time())}
                    inboxDB.insert_one(post)

async def setup(bot):
    await bot.add_cog(_inboxProtection(bot))
