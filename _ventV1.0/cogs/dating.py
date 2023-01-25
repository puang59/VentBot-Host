from unittest import result
from discord.ext import commands
import asyncio
import discord 
from random import *
from pymongo import MongoClient, message

class dating(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    global cluster
    global db
    global collection
    global inbox
    global gChat
    global dHistory
    cluster = MongoClient(
        "mongodb+srv://Edryu:jaisairam4@cluster0.inbe1.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = cluster["Dating"]
    collection = db["DatingProfile"]
    inbox = db['DatingInbox']
    gChat = db['DatingGlobal']
    dHistory = db['DatingHistory']


    global boyAV 
    global girlAV
    global otherAV
    boyAV = ['https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/adult_people_avatar_man_male_employee_tie-256.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/boy_people._avatar_man_male_teenager_user__1-128.png',
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/man_adult_mustache_people_woman_father_avatar-256.png',
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/boy_people_avatar_man_male_teenager_handsome-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/boy_people_avatar_man_male_teenager_hood-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/glasses_businessman_people_male_man_avatar_blonde-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/boy_people._avatar_man_male_teenager_user_-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/male_glasses_hacker_people_man_programmer_avatar-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/male_leader_manager_people_man_boss_avatar-2-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/boy_people_avatar_man_male_hat_handsome-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/boy_people_avatar_man_male_young_handsome-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/boy_people_avatar_man_male_freckles_ginger-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/boy_people_avatar_man_male_teenager_handsome_3-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/boy_people_avatar_man_male_teenager_ear_piercing-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/boy_people_avatar_man_male_teenager_handsome_user-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/Arab_adult_people_beard_Islam_avatar_man-128.png']

    girlAV = ['https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/girl_female_young_people_woman_teenager_avatar-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/girl_young_female_people_woman_teenager_avatar-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/girl_female_adult_people_woman_doctor_avatar-2-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/girl_ginger_glasses_people_woman_teenager_avatar-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/girl_long_hair_beautiful_people_woman_teenager_avatar-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/girl_ginger_curly__people_woman_teenager_avatar-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/girl_blonde_curl_people_woman_teenager_avatar-2-128.png',
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/skin_head_african_earring_girl_young_woman_avatar-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/girl_ponytail_people_woman_teenager_avatar_cute-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/girl_long_hair_female_people_woman_user_avatar-2-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/female_african_dreadlocks_girl_young_woman_avatar-2-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/girl_blonde_pony_tail_people_woman_teenager_avatar-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/girl_Islam_beautiful_people_woman_hijab_avatar-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/girl_bobtay_people_woman_teenager_avatar_user-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/girl_long_hair_female_people_woman_teenager_avatar-128.png',    
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/girl_ponytail_people_woman_teenager_avatar_female-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/girl_ponytail_people_woman_teenager_avatar_portrait-128.png',
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/girl_adult_beautiful_people_woman_mother_avatar-128.png']


    otherAV = ['https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/adult_people_avatar_man_male_employee_tie-256.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/girl_female_young_people_woman_teenager_avatar-128.png',
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/boy_people._avatar_man_male_teenager_user__1-128.png',
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/girl_young_female_people_woman_teenager_avatar-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/man_adult_mustache_people_woman_father_avatar-256.png',
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/girl_female_adult_people_woman_doctor_avatar-2-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/boy_people_avatar_man_male_teenager_handsome-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/girl_ginger_glasses_people_woman_teenager_avatar-128.png',
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/boy_people_avatar_man_male_teenager_hood-128.png',
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/girl_long_hair_beautiful_people_woman_teenager_avatar-128.png',  
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/boy_people_avatar_man_male_teenager_hood-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/girl_long_hair_beautiful_people_woman_teenager_avatar-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/glasses_businessman_people_male_man_avatar_blonde-128.png',
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/girl_ginger_curly__people_woman_teenager_avatar-128.png',
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/glasses_businessman_people_male_man_avatar_blonde-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/girl_blonde_curl_people_woman_teenager_avatar-2-128.png',
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/glasses_businessman_people_male_man_avatar_blonde-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/skin_head_african_earring_girl_young_woman_avatar-128.png',
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/boy_people._avatar_man_male_teenager_user_-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/girl_ponytail_people_woman_teenager_avatar_cute-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/male_glasses_hacker_people_man_programmer_avatar-128.png',  
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/girl_long_hair_female_people_woman_user_avatar-2-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/female_african_dreadlocks_girl_young_woman_avatar-2-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/boy_people_avatar_man_male_hat_handsome-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/female_african_dreadlocks_girl_young_woman_avatar-2-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/boy_people_avatar_man_male_young_handsome-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/girl_blonde_pony_tail_people_woman_teenager_avatar-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/boy_people_avatar_man_male_teenager_handsome_3-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/girl_Islam_beautiful_people_woman_hijab_avatar-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/boy_people_avatar_man_male_freckles_ginger-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/girl_bobtay_people_woman_teenager_avatar_user-128.png',
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/boy_people_avatar_man_male_teenager_handsome_3-128.png',  
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/girl_long_hair_female_people_woman_teenager_avatar-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/boy_people_avatar_man_male_teenager_ear_piercing-128.png',  
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/girl_ponytail_people_woman_teenager_avatar_female-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/girl_ponytail_people_woman_teenager_avatar_portrait-128.png',
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/girl_adult_beautiful_people_woman_mother_avatar-128.png' ,
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/boy_people_avatar_man_male_teenager_ear_piercing-128.png', 
    'https://cdn4.iconfinder.com/data/icons/people-avatar-filled-outline/64/boy_people_avatar_man_male_teenager_handsome_user-128.png' ]

    # Globalising a var LOL
    # @commands.command()
    # async def assign(self, ctx):
    #     global genChannel
    #     genChannel = self.bot.get_channel(999682901786505336)

    global cycleButton
    class cycleButton(discord.ui.View):
        def __init__(self, *, timeout=180):
            super().__init__(timeout=timeout)
        @discord.ui.button(style=discord.ButtonStyle.grey, disabled=False, emoji='⬅️')
        async def backward(self, interaction:discord.Interaction, button:discord.ui.Button):
            collection.update_one({"_id": interaction.user.id}, {"$inc": {"avatar": -1}})
            results = collection.find_one({"_id": interaction.user.id})
            # Setting embed color
            if results['gender'].lower() == "male" or results['gender'].lower() == "boy":
                value = 0x00caff
                if collection.find_one({"_id": interaction.user.id}):  
                    pEmbed= discord.Embed(color = value)
                    pEmbed.set_author(
                        name="Profile")
                    pEmbed.add_field(
                        name="Age:", value=results["age"])
                    pEmbed.add_field(
                        name="Gender:", value=results["gender"])
                    pEmbed.add_field(
                            name="Sexuality:", value=results["sexuality"])
                    pEmbed.add_field(
                        name="Interests:", value=results["interests"], inline=False)
                    if results['gender'].lower() == "male" or results['gender'].lower() == "boy":
                        pEmbed.set_thumbnail(url=boyAV[results['avatar']])
                    await interaction.response.edit_message(embed=pEmbed)
            elif results['gender'].lower() == "female" or results['gender'].lower() == 'girl':
                value = 0xff95ff
                if collection.find_one({"_id": interaction.user.id}):  
                    pEmbed= discord.Embed(color = value)
                    pEmbed.set_author(
                        name="Profile")
                    pEmbed.add_field(
                        name="Age:", value=results["age"])
                    pEmbed.add_field(
                        name="Gender:", value=results["gender"])
                    pEmbed.add_field(
                            name="Sexuality:", value=results["sexuality"])
                    pEmbed.add_field(
                        name="Interests:", value=results["interests"], inline=False)
                    if results['gender'].lower() == "female" or results['gender'].lower() == "girl":
                        pEmbed.set_thumbnail(url=girlAV[results['avatar']])
                    await interaction.response.edit_message(embed=pEmbed)
            else: # non-binary
                value = randint(0, 0xffffff)
                if collection.find_one({"_id": interaction.user.id}):  
                    pEmbed= discord.Embed(color = value)
                    pEmbed.set_author(
                        name="Profile")
                    pEmbed.add_field(
                        name="Age:", value=results["age"])
                    pEmbed.add_field(
                        name="Gender:", value=results["gender"])
                    pEmbed.add_field(
                            name="Sexuality:", value=results["sexuality"])
                    pEmbed.add_field(
                        name="Interests:", value=results["interests"], inline=False)
                    pEmbed.set_thumbnail(url=otherAV[results['avatar']])
                    await interaction.response.edit_message(embed=pEmbed)

        @discord.ui.button(style=discord.ButtonStyle.grey, disabled=False, emoji='➡️')
        async def forward(self, interaction:discord.Interaction, button:discord.ui.Button):
            collection.update_one({"_id": interaction.user.id}, {"$inc": {"avatar": 1}})
            results = collection.find_one({"_id": interaction.user.id})
            # Setting embed color
            if results['gender'].lower() == "male" or results['gender'].lower() == "boy":
                value = 0x00caff
                if collection.find_one({"_id": interaction.user.id}):  
                    pEmbed= discord.Embed(color = value)
                    pEmbed.set_author(
                        name="Profile")
                    pEmbed.add_field(
                        name="Age:", value=results["age"])
                    pEmbed.add_field(
                        name="Gender:", value=results["gender"])
                    pEmbed.add_field(
                            name="Sexuality:", value=results["sexuality"])
                    pEmbed.add_field(
                        name="Interests:", value=results["interests"], inline=False)
                    if results['gender'].lower() == "male" or results['gender'].lower() == "boy":
                        pEmbed.set_thumbnail(url=boyAV[results['avatar']])
                    await interaction.response.edit_message(embed=pEmbed)
            elif results['gender'].lower() == "female" or results['gender'].lower() == 'girl':
                value = 0xff95ff
                if collection.find_one({"_id": interaction.user.id}):  
                    pEmbed= discord.Embed(color = value)
                    pEmbed.set_author(
                        name="Profile")
                    pEmbed.add_field(
                        name="Age:", value=results["age"])
                    pEmbed.add_field(
                        name="Gender:", value=results["gender"])
                    pEmbed.add_field(
                            name="Sexuality:", value=results["sexuality"])
                    pEmbed.add_field(
                        name="Interests:", value=results["interests"], inline=False)
                    if results['gender'].lower() == "female" or results['gender'].lower() == "girl":
                        pEmbed.set_thumbnail(url=girlAV[results['avatar']])
                    await interaction.response.edit_message(embed=pEmbed)
            else: # non-binary
                value = randint(0, 0xffffff)
                if collection.find_one({"_id": interaction.user.id}):  
                    pEmbed= discord.Embed(color = value)
                    pEmbed.set_author(
                        name="Profile")
                    pEmbed.add_field(
                        name="Age:", value=results["age"])
                    pEmbed.add_field(
                        name="Gender:", value=results["gender"])
                    pEmbed.add_field(
                            name="Sexuality:", value=results["sexuality"])
                    pEmbed.add_field(
                        name="Interests:", value=results["interests"], inline=False)
                    pEmbed.set_thumbnail(url=otherAV[results['avatar']])
                    await interaction.response.edit_message(embed=pEmbed)

        @discord.ui.button(label="Done",style=discord.ButtonStyle.green, disabled=False, emoji='👍')
        async def done_button(self, interaction:discord.Interaction, button:discord.ui.Button):
            await interaction.channel.send("<:agree:943603027313565757> Thank you! Introduction posted successfully in <#999682901786505336>.\n\n**Note:** You can always edit your intro by using command `.intro`")
            results = collection.find_one({"_id": interaction.user.id})
            # Setting embed color
            if results['gender'].lower() == "male" or results['gender'].lower() == "boy":
                value = 0x00caff
                if collection.find_one({"_id": interaction.user.id}):  
                    embed= discord.Embed(color = value)
                    embed.set_author(
                        name="Profile")
                    embed.add_field(
                        name="Age:", value=results["age"])
                    embed.add_field(
                        name="Gender:", value=results["gender"])
                    embed.add_field(
                            name="Sexuality:", value=results["sexuality"])
                    embed.add_field(
                        name="Interests:", value=results["interests"], inline=False)
                    if results['gender'].lower() == "male" or results['gender'].lower() == "boy":
                        embed.set_thumbnail(url=boyAV[results['avatar']])
                    collection.update_one({"_id": interaction.user.id}, {"$set": {"avatarURL": boyAV[results['avatar']]}})
            elif results['gender'].lower() == "female" or results['gender'].lower() == 'girl':
                value = 0xff95ff
                if collection.find_one({"_id": interaction.user.id}):  
                    embed= discord.Embed(color = value)
                    embed.set_author(
                        name="Profile")
                    embed.add_field(
                        name="Age:", value=results["age"])
                    embed.add_field(
                        name="Gender:", value=results["gender"])
                    embed.add_field(
                            name="Sexuality:", value=results["sexuality"])
                    embed.add_field(
                        name="Interests:", value=results["interests"], inline=False)
                    if results['gender'].lower() == "female" or results['gender'].lower() == "girl":
                        embed.set_thumbnail(url=girlAV[results['avatar']])
                    collection.update_one({"_id": interaction.user.id}, {"$set": {"avatarURL": girlAV[results['avatar']]}})
            else: # non-binary
                value = randint(0, 0xffffff)
                if collection.find_one({"_id": interaction.user.id}):  
                    embed= discord.Embed(color = value)
                    embed.set_author(
                        name="Profile")
                    embed.add_field(
                        name="Age:", value=results["age"])
                    embed.add_field(
                        name="Gender:", value=results["gender"])
                    embed.add_field(
                            name="Sexuality:", value=results["sexuality"])
                    embed.add_field(
                        name="Interests:", value=results["interests"], inline=False)
                    embed.set_thumbnail(url=otherAV[results['avatar']])

                    collection.update_one({"_id": interaction.user.id}, {"$set": {"avatarURL": otherAV[results['avatar']]}})

            genChannel = interaction.guild.get_channel(999682901786505336)

            try:
                txt = await genChannel.fetch_message(results["msg_id"])
                await txt.edit(embed=embed)
                await interaction.message.delete()
                collection.update_one({"_id": interaction.user.id}, {
                                    "$set": {"msg_id": txt.id}})
            except: 
                xx = await genChannel.send(embed=embed)
                await xx.add_reaction("💌")
                await interaction.message.delete()
                collection.update_one({"_id": interaction.user.id}, {
                                    "$set": {"msg_id": xx.id}})

            # Age checker 
            if int(results['age']) < 13:
                try:
                    await interaction.user.send("Sorry! You little too young for both discord and dating")
                except:
                    pass
                user = interaction.guild.get_member(results['_id'])
                await user.kick(reason="Underage")
                
    global repButton
    class repButton(discord.ui.View):
        def __init__(self, *, timeout=3600):
            super().__init__(timeout=timeout)
        @discord.ui.button(label="Report User",style=discord.ButtonStyle.danger, disabled=False)
        async def gray_button(self, interaction:discord.Interaction, button:discord.ui.Button):
            button.disabled=True
            button.label="Reported"
            button.style=discord.ButtonStyle.gray
            await interaction.response.edit_message(view=self)

            data = inbox.find_one({"reactor":interaction.user.id})
            channel = interaction.client.get_channel(1000432578320400404)
            if inbox.find_one({"reactor":interaction.user.id}):
                author = interaction.client.get_user(int(data['author']))

                interChn = interaction.client.get_channel(interaction.channel_id)
                txt = await interChn.fetch_message(interaction.message.id)
                em = discord.Embed(description=f"{txt.embeds[0].description}")

                em.set_author(name=f"{author.name} - {data['author']}", icon_url=f"{author.avatar.url}")
                await channel.send(f"{interaction.channel.name} - <#{interaction.channel_id}>", embed=em)
                await interaction.channel.send(content="<:agree:943603027313565757> The user has been reported to the staff team.")
                #blocking the reported user 
                topic = interaction.channel.topic
                chn = interaction.guild.get_channel(int(topic))
                #await chn.set_permissions(author, send_messages=False, view_channel=True)
                await chn.edit(topic=f"{chn.topic}"+" REPORTED")
                await interaction.channel.edit(topic=f"{interaction.channel.topic}"+" Reporter")
                await chn.send("You have been reported by the person your were talking to! We are looking into the matter and will get back to you soon.")

                #Blocking users
                repoterUser = interaction.client.get_user(data['reactor'])
                await interaction.channel.set_permissions(repoterUser, send_messages=False, view_channel=True)
                reportedUser = interaction.client.get_user(data['author'])
                await chn.set_permissions(reportedUser, send_messages=False, view_channel=True)
            elif inbox.find_one({"author":interaction.user.id}):
                data = inbox.find_one({"author":interaction.user.id})
                reactor = interaction.client.get_user(int(data['reactor']))

                interChn = interaction.client.get_channel(interaction.channel_id)
                txt = await interChn.fetch_message(interaction.message.id)
                em = discord.Embed(description=f"{txt.embeds[0].description}")

                em.set_author(name=f"{reactor.name} - {data['reactor']}", icon_url=f"{reactor.avatar.url}")
                await channel.send(f"{interaction.channel.name} - <#{interaction.channel_id}>", embed=em)
                await interaction.channel.send(content="<:agree:943603027313565757> The user has been reported to the staff team.")
                #blocking the reported user 
                topic = interaction.channel.topic
                chn = interaction.guild.get_channel(int(topic))
                #await chn.set_permissions(reactor, send_messages=False, view_channel=True)
                await chn.edit(topic=f"{chn.topic}"+" REPORTED")
                await interaction.channel.edit(topic=f"{interaction.channel.topic}"+" Reporter")
                await chn.send("You have been reported by the person your were talking to! We are looking into the matter and will get back to you soon.")

                #Blocking users
                repoterUser = interaction.client.get_user(data['author'])
                await interaction.channel.set_permissions(repoterUser, send_messages=False, view_channel=True)
                reportedUser = interaction.client.get_user(data['reactor'])
                await chn.set_permissions(reportedUser, send_messages=False, view_channel=True)
            else: 
                await interaction.channel.send("UhOh! Looks like something went wrong. Please DM me to report the user instead.")

            # Blocking both of them from sending message
            # man1 = interaction.client.get_user(data['author'])
            # await chn.set_permissions(man1, send_messages=False, view_channel=False)
            # await interChn.set_permissions(man1, send_messages=False, view_channel=False)
            # man = interaction.client.get_user(data['reactor'])
            # await interChn.set_permissions(man, send_messages=False, view_channel=False)
            # await chn.set_permissions(man, send_messages=False, view_channel=False)

    
    #     channel = message.channel
    #     await channel.create_thread(name=f"{message.author.discriminator}-{message.author.name}", message=message, auto_archive_duration=1440, reason=None)
    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        if member.guild.id == 999682901308342342:
            if collection.find_one({"author_id": member.id}):
                data = collection.find_one({"author_id": member.id})
                ch = self.bot.get_channel(int(data["channel_id"]))
                await ch.set_permissions(member, send_messages=True, view_channel=True)
            else:
                try: 
                    user_a = member

                    categ = discord.utils.get(guild.categories, name="PRIVATE SPACE")
                    text_channel = await categ.create_text_channel(f"{member.name}s - {member.discriminator}")
                    await text_channel.set_permissions(user_a, send_messages=True, view_channel=True)
                    await text_channel.set_permissions(guild.default_role, send_messages=False, view_channel=False)
                    await text_channel.edit(topic=f"Custom PRIVATE channel for {member.name}")
                    await text_channel.edit(slowmode_delay=7200)

                    ema = discord.Embed(
                        description="Please access the `thread channel` to post your profile!"
                    )
                    a = await text_channel.send(f"Welcome {member.mention}!  (≧◡≦)", embed=ema)
                    thre = await text_channel.create_thread(name=f"Intro - {member.name}", message=a, auto_archive_duration=1440, reason=None)

                    if collection.find_one({"_id": member.id}):
                        await thre.send('Your Intro has already been posted! Type `.intro` to update your old intro.')
                    else: 
                        def check_join(msg):
                            return msg.author == member

                        await thre.send("What is your gender? [Male, Female, Non-Binary]")

                        try:
                            msg2 = await self.bot.wait_for("message", check=check_join, timeout=300)
                        except asyncio.TimeoutError:
                            error3 = await thre.send("<:disagree:943603027854626816> Introduction process failed")
                            await asyncio.sleep(5)
                            await error3.delete()
                            return
                        if msg2: 
                            await thre.send('What is your sexuality?')

                            try:
                                msg1 = await self.bot.wait_for("message", check=check_join, timeout=300)
                            except asyncio.TimeoutError:
                                error5 = await thre.send("<:disagree:943603027854626816> Introduction process failed")
                                await asyncio.sleep(5)
                                await error5.delete()
                                return
                            if msg1:
                                await thre.send("How old are you?")

                                try:
                                    msg3 = await self.bot.wait_for("message", check=check_join, timeout=300)
                                except asyncio.TimeoutError:
                                    error5 = await thre.send("<:disagree:943603027854626816> Introduction process failed")
                                    await asyncio.sleep(5)
                                    await error5.delete()
                                    return

                                if msg3:
                                    await thre.send("Alright last question. What are your interests?")

                                    try:
                                        msg6 = await self.bot.wait_for("message", check=check_join, timeout=300)
                                    except asyncio.TimeoutError:
                                        error8 = await thre.send("<:disagree:943603027854626816> Introduction process failed")
                                        await asyncio.sleep(5)
                                        await error8.delete()
                                        return

                                    if msg6:
                                        writeDocument = 0
                                        post = {"_id": member.id, "ident": "dating-vent", "avatar": writeDocument, "name": member.name,
                                                "age": msg3.content, "gender": msg2.content, 'sexuality': msg1.content, "interests": msg6.content}
                                        if collection.find_one({"_id": member.id}):
                                            collection.update_many({"_id": member.id}, {"$set": {"avatar": writeDocument, "name": member.name,
                                                "age": msg3.content, "gender": msg2.content, 'sexuality': msg1.content, "interests": msg6.content}})
                                        else:
                                            collection.insert_one(post)

                                        results = collection.find_one({"_id": member.id})

                                        # Setting embed color
                                        if results['gender'].lower() == "male" or results['gender'].lower() == "boy":
                                            value = 0x00caff
                                            pEmbed= discord.Embed(color = value)
                                            pEmbed.set_author(
                                                name="Profile")
                                            pEmbed.add_field(
                                                name="Age:", value=results["age"])
                                            pEmbed.add_field(
                                                name="Gender:", value=results["gender"])
                                            pEmbed.add_field(
                                                    name="Sexuality:", value=results["sexuality"])
                                            pEmbed.add_field(
                                                name="Interests:", value=results["interests"], inline=False)
                                            if results['gender'].lower() == "male" or results['gender'].lower() == "boy":
                                                pEmbed.set_thumbnail(url=boyAV[results['avatar']])

                                            await thre.send("Preview:", embed = pEmbed, view=cycleButton())

                                        elif results['gender'].lower() == "female" or results['gender'].lower() == 'girl':
                                            value = 0xff95ff
                                            pEmbed= discord.Embed(color = value)
                                            pEmbed.set_author(
                                                name="Profile")
                                            pEmbed.add_field(
                                                name="Age:", value=results["age"])
                                            pEmbed.add_field(
                                                name="Gender:", value=results["gender"])
                                            pEmbed.add_field(
                                                    name="Sexuality:", value=results["sexuality"])
                                            pEmbed.add_field(
                                                name="Interests:", value=results["interests"], inline=False)
                                            if results['gender'].lower() == "female" or results['gender'].lower() == "girl":
                                                pEmbed.set_thumbnail(url=girlAV[results['avatar']])

                                            await thre.send("Preview:", embed = pEmbed, view=cycleButton())
                                        else: #non-binary
                                            value = randint(0, 0xffffff)
                                            pEmbed= discord.Embed(color = value)
                                            pEmbed.set_author(
                                                name="Profile")
                                            pEmbed.add_field(
                                                name="Age:", value=results["age"])
                                            pEmbed.add_field(
                                                name="Gender:", value=results["gender"])
                                            pEmbed.add_field(
                                                    name="Sexuality:", value=results["sexuality"])
                                            pEmbed.add_field(
                                                name="Interests:", value=results["interests"], inline=False)
                                            pEmbed.set_thumbnail(url=otherAV[results['avatar']])

                                            await thre.send("Preview:", embed = pEmbed, view=cycleButton())
                                        # await thre.send("<:agree:943603027313565757> Thank you! Introduction posted successfully in <#999682901786505336>.\n\n**Note:** You can always edit your intro by using command `.intro`")

                                        # embed = discord.Embed(color=value)
                                        # embed.set_author(
                                        #     name="Profile")
                                        # embed.add_field(
                                        #     name="Age:", value=results["age"])
                                        # embed.add_field(
                                        #     name="Gender:", value=results["gender"])
                                        # embed.add_field(
                                        #     name="Interests:", value=results["interests"], inline=False)
                                        # embed.set_thumbnail(
                                        #     url='https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fvectorified.com%2Fimages%2Fperson-icon-white-10.png&f=1&nofb=1')
                                        # a = self.bot.get_channel(
                                        #     999682901786505336)
                                        # xx = await a.send(embed=embed)
                                        # await xx.add_reaction("💌")

                                        # collection.update_one({"_id": member.id}, {
                                        #                     "$set": {"msg_id": xx.id}})

                except: 
                    try: 
                        user_a = member

                        categ = discord.utils.get(guild.categories, name="PRIVATE SPACE (2)")
                        text_channel = await categ.create_text_channel(f"{member.name}s - {member.discriminator}")
                        await text_channel.set_permissions(user_a, send_messages=True, view_channel=True)
                        await text_channel.set_permissions(guild.default_role, send_messages=False, view_channel=False)
                        await text_channel.edit(topic=f"Custom PRIVATE channel for {member.name}")
                        await text_channel.edit(slowmode_delay=7200)

                        ema = discord.Embed(
                            description="Please access the `thread channel` to post your profile!"
                        )
                        a = await text_channel.send(f"Welcome {member.mention}!  (≧◡≦)", embed=ema)
                        thre = await text_channel.create_thread(name=f"Intro - {member.name}", message=a, auto_archive_duration=1440, reason=None)

                        if collection.find_one({"_id": member.id}):
                            await thre.send('Your Intro has already been posted! Type `.intro` to update your old intro.')
                        else: 
                            def check_join(msg):
                                return msg.author == member

                            await thre.send("What is your gender? [Male, Female, Non-Binary]")

                            try:
                                msg2 = await self.bot.wait_for("message", check=check_join, timeout=300)
                            except asyncio.TimeoutError:
                                error3 = await thre.send("<:disagree:943603027854626816> Introduction process failed")
                                await asyncio.sleep(5)
                                await error3.delete()
                                return

                            if msg2: 
                                await thre.send('What is your sexuality?')

                                try:
                                    msg1 = await self.bot.wait_for("message", check=check_join, timeout=300)
                                except asyncio.TimeoutError:
                                    error5 = await thre.send("<:disagree:943603027854626816> Introduction process failed")
                                    await asyncio.sleep(5)
                                    await error5.delete()
                                    return
                                if msg1:
                                    await thre.send("How old are you?")

                                    try:
                                        msg3 = await self.bot.wait_for("message", check=check_join, timeout=300)
                                    except asyncio.TimeoutError:
                                        error5 = await thre.send("<:disagree:943603027854626816> Introduction process failed")
                                        await asyncio.sleep(5)
                                        await error5.delete()
                                        return

                                    if msg3:
                                        await thre.send("Alright last question. What are your interests?")

                                        try:
                                            msg6 = await self.bot.wait_for("message", check=check_join, timeout=300)
                                        except asyncio.TimeoutError:
                                            error8 = await thre.send("<:disagree:943603027854626816> Introduction process failed")
                                            await asyncio.sleep(5)
                                            await error8.delete()
                                            return

                                        if msg6:
                                            writeDocument = 0
                                            post = {"_id": member.id, "ident": "dating-vent", "avatar": writeDocument, "name": member.name,
                                                    "age": msg3.content, "gender": msg2.content, "interests": msg6.content}
                                            if collection.find_one({"_id": member.id}):
                                                collection.update_many({"_id": member.id}, {"$set": {"avatar": writeDocument, "name": member.name,
                                                    "age": msg3.content, "gender": msg2.content, "interests": msg6.content}})
                                            else:
                                                collection.insert_one(post)

                                            results = collection.find_one({"_id": member.id})

                                            # Setting embed color
                                            if results['gender'].lower() == "male" or results['gender'].lower() == "boy":
                                                value = 0x00caff
                                                pEmbed= discord.Embed(color = value)
                                                pEmbed.set_author(
                                                    name="Profile")
                                                pEmbed.add_field(
                                                    name="Age:", value=results["age"])
                                                pEmbed.add_field(
                                                    name="Gender:", value=results["gender"])
                                                pEmbed.add_field(
                                                    name="Interests:", value=results["interests"], inline=False)
                                                if results['gender'].lower() == "male" or results['gender'].lower() == "boy":
                                                    pEmbed.set_thumbnail(url=boyAV[results['avatar']])

                                                await thre.send("Preview:", embed = pEmbed, view=cycleButton())

                                            elif results['gender'].lower() == "female" or results['gender'].lower() == 'girl':
                                                value = 0xff95ff
                                                pEmbed= discord.Embed(color = value)
                                                pEmbed.set_author(
                                                    name="Profile")
                                                pEmbed.add_field(
                                                    name="Age:", value=results["age"])
                                                pEmbed.add_field(
                                                    name="Gender:", value=results["gender"])
                                                pEmbed.add_field(
                                                    name="Interests:", value=results["interests"], inline=False)
                                                if results['gender'].lower() == "female" or results['gender'].lower() == "girl":
                                                    pEmbed.set_thumbnail(url=girlAV[results['avatar']])

                                                await thre.send("Preview:", embed = pEmbed, view=cycleButton())
                                            else: #non-binary
                                                value = randint(0, 0xffffff)
                                                pEmbed= discord.Embed(color = value)
                                                pEmbed.set_author(
                                                    name="Profile")
                                                pEmbed.add_field(
                                                    name="Age:", value=results["age"])
                                                pEmbed.add_field(
                                                    name="Gender:", value=results["gender"])
                                                pEmbed.add_field(
                                                    name="Interests:", value=results["interests"], inline=False)
                                                pEmbed.set_thumbnail(url=otherAV[results['avatar']])

                                                await thre.send("Preview:", embed = pEmbed, view=cycleButton())
                    except: 
                        try: 
                            user_a = member

                            categ = discord.utils.get(guild.categories, name="PRIVATE SPACE (3)")
                            text_channel = await categ.create_text_channel(f"{member.name}s - {member.discriminator}")
                            await text_channel.set_permissions(user_a, send_messages=True, view_channel=True)
                            await text_channel.set_permissions(guild.default_role, send_messages=False, view_channel=False)
                            await text_channel.edit(topic=f"Custom PRIVATE channel for {member.name}")
                            await text_channel.edit(slowmode_delay=7200)

                            ema = discord.Embed(
                                description="Please access the `thread channel` to post your profile!"
                            )
                            a = await text_channel.send(f"Welcome {member.mention}!  (≧◡≦)", embed=ema)
                            thre = await text_channel.create_thread(name=f"Intro - {member.name}", message=a, auto_archive_duration=1440, reason=None)

                            if collection.find_one({"_id": member.id}):
                                await thre.send('Your Intro has already been posted! Type `.intro` to update your old intro.')
                            else: 
                                def check_join(msg):
                                    return msg.author == member

                                await thre.send("What is your gender? [Male, Female, Non-Binary]")

                                try:
                                    msg2 = await self.bot.wait_for("message", check=check_join, timeout=300)
                                except asyncio.TimeoutError:
                                    error3 = await thre.send("<:disagree:943603027854626816> Introduction process failed")
                                    await asyncio.sleep(5)
                                    await error3.delete()
                                    return

                                if msg2: 
                                    await thre.send('What is your sexuality?')

                                    try:
                                        msg1 = await self.bot.wait_for("message", check=check_join, timeout=300)
                                    except asyncio.TimeoutError:
                                        error5 = await thre.send("<:disagree:943603027854626816> Introduction process failed")
                                        await asyncio.sleep(5)
                                        await error5.delete()
                                        return
                                    if msg1:
                                        await thre.send("How old are you?")

                                        try:
                                            msg3 = await self.bot.wait_for("message", check=check_join, timeout=300)
                                        except asyncio.TimeoutError:
                                            error5 = await thre.send("<:disagree:943603027854626816> Introduction process failed")
                                            await asyncio.sleep(5)
                                            await error5.delete()
                                            return

                                        if msg3:
                                            await thre.send("Alright last question. What are your interests?")

                                            try:
                                                msg6 = await self.bot.wait_for("message", check=check_join, timeout=300)
                                            except asyncio.TimeoutError:
                                                error8 = await thre.send("<:disagree:943603027854626816> Introduction process failed")
                                                await asyncio.sleep(5)
                                                await error8.delete()
                                                return

                                            if msg6:
                                                writeDocument = 0
                                                post = {"_id": member.id, "ident": "dating-vent", "avatar": writeDocument, "name": member.name,
                                                        "age": msg3.content, "gender": msg2.content, "interests": msg6.content}
                                                if collection.find_one({"_id": member.id}):
                                                    collection.update_many({"_id": member.id}, {"$set": {"avatar": writeDocument, "name": member.name,
                                                        "age": msg3.content, "gender": msg2.content, "interests": msg6.content}})
                                                else:
                                                    collection.insert_one(post)

                                                results = collection.find_one({"_id": member.id})

                                                # Setting embed color
                                                if results['gender'].lower() == "male" or results['gender'].lower() == "boy":
                                                    value = 0x00caff
                                                    pEmbed= discord.Embed(color = value)
                                                    pEmbed.set_author(
                                                        name="Profile")
                                                    pEmbed.add_field(
                                                        name="Age:", value=results["age"])
                                                    pEmbed.add_field(
                                                        name="Gender:", value=results["gender"])
                                                    pEmbed.add_field(
                                                        name="Interests:", value=results["interests"], inline=False)
                                                    if results['gender'].lower() == "male" or results['gender'].lower() == "boy":
                                                        pEmbed.set_thumbnail(url=boyAV[results['avatar']])

                                                    await thre.send("Preview:", embed = pEmbed, view=cycleButton())

                                                elif results['gender'].lower() == "female" or results['gender'].lower() == 'girl':
                                                    value = 0xff95ff
                                                    pEmbed= discord.Embed(color = value)
                                                    pEmbed.set_author(
                                                        name="Profile")
                                                    pEmbed.add_field(
                                                        name="Age:", value=results["age"])
                                                    pEmbed.add_field(
                                                        name="Gender:", value=results["gender"])
                                                    pEmbed.add_field(
                                                        name="Interests:", value=results["interests"], inline=False)
                                                    if results['gender'].lower() == "female" or results['gender'].lower() == "girl":
                                                        pEmbed.set_thumbnail(url=girlAV[results['avatar']])

                                                    await thre.send("Preview:", embed = pEmbed, view=cycleButton())
                                                else: #non-binary
                                                    value = randint(0, 0xffffff)
                                                    pEmbed= discord.Embed(color = value)
                                                    pEmbed.set_author(
                                                        name="Profile")
                                                    pEmbed.add_field(
                                                        name="Age:", value=results["age"])
                                                    pEmbed.add_field(
                                                        name="Gender:", value=results["gender"])
                                                    pEmbed.add_field(
                                                        name="Interests:", value=results["interests"], inline=False)
                                                    pEmbed.set_thumbnail(url=otherAV[results['avatar']])

                                                    await thre.send("Preview:", embed = pEmbed, view=cycleButton())
                        except: 
                            try: 
                                user_a = member

                                categ = discord.utils.get(guild.categories, name="PRIVATE SPACE (4)")
                                text_channel = await categ.create_text_channel(f"{member.name}s - {member.discriminator}")
                                await text_channel.set_permissions(user_a, send_messages=True, view_channel=True)
                                await text_channel.set_permissions(guild.default_role, send_messages=False, view_channel=False)
                                await text_channel.edit(topic=f"Custom PRIVATE channel for {member.name}")
                                await text_channel.edit(slowmode_delay=7200)

                                ema = discord.Embed(
                                    description="Please access the `thread channel` to post your profile!"
                                )
                                a = await text_channel.send(f"Welcome {member.mention}!  (≧◡≦)", embed=ema)
                                thre = await text_channel.create_thread(name=f"Intro - {member.name}", message=a, auto_archive_duration=1440, reason=None)

                                if collection.find_one({"_id": member.id}):
                                    await thre.send('Your Intro has already been posted! Type `.intro` to update your old intro.')
                                else: 
                                    def check_join(msg):
                                        return msg.author == member

                                    await thre.send("What is your gender? [Male, Female, Non-Binary]")

                                    try:
                                        msg2 = await self.bot.wait_for("message", check=check_join, timeout=300)
                                    except asyncio.TimeoutError:
                                        error3 = await thre.send("<:disagree:943603027854626816> Introduction process failed")
                                        await asyncio.sleep(5)
                                        await error3.delete()
                                        return

                                    if msg2: 
                                        await thre.send('What is your sexuality?')

                                        try:
                                            msg1 = await self.bot.wait_for("message", check=check_join, timeout=300)
                                        except asyncio.TimeoutError:
                                            error5 = await thre.send("<:disagree:943603027854626816> Introduction process failed")
                                            await asyncio.sleep(5)
                                            await error5.delete()
                                            return
                                        if msg1:
                                            await thre.send("How old are you?")

                                            try:
                                                msg3 = await self.bot.wait_for("message", check=check_join, timeout=300)
                                            except asyncio.TimeoutError:
                                                error5 = await thre.send("<:disagree:943603027854626816> Introduction process failed")
                                                await asyncio.sleep(5)
                                                await error5.delete()
                                                return

                                            if msg3:
                                                await thre.send("Alright last question. What are your interests?")

                                                try:
                                                    msg6 = await self.bot.wait_for("message", check=check_join, timeout=300)
                                                except asyncio.TimeoutError:
                                                    error8 = await thre.send("<:disagree:943603027854626816> Introduction process failed")
                                                    await asyncio.sleep(5)
                                                    await error8.delete()
                                                    return

                                                if msg6:
                                                    writeDocument = 0
                                                    post = {"_id": member.id, "ident": "dating-vent", "avatar": writeDocument, "name": member.name,
                                                            "age": msg3.content, "gender": msg2.content, "interests": msg6.content}
                                                    if collection.find_one({"_id": member.id}):
                                                        collection.update_many({"_id": member.id}, {"$set": {"avatar": writeDocument, "name": member.name,
                                                            "age": msg3.content, "gender": msg2.content, "interests": msg6.content}})
                                                    else:
                                                        collection.insert_one(post)

                                                    results = collection.find_one({"_id": member.id})

                                                    # Setting embed color
                                                    if results['gender'].lower() == "male" or results['gender'].lower() == "boy":
                                                        value = 0x00caff
                                                        pEmbed= discord.Embed(color = value)
                                                        pEmbed.set_author(
                                                            name="Profile")
                                                        pEmbed.add_field(
                                                            name="Age:", value=results["age"])
                                                        pEmbed.add_field(
                                                            name="Gender:", value=results["gender"])
                                                        pEmbed.add_field(
                                                            name="Interests:", value=results["interests"], inline=False)
                                                        if results['gender'].lower() == "male" or results['gender'].lower() == "boy":
                                                            pEmbed.set_thumbnail(url=boyAV[results['avatar']])

                                                        await thre.send("Preview:", embed = pEmbed, view=cycleButton())

                                                    elif results['gender'].lower() == "female" or results['gender'].lower() == 'girl':
                                                        value = 0xff95ff
                                                        pEmbed= discord.Embed(color = value)
                                                        pEmbed.set_author(
                                                            name="Profile")
                                                        pEmbed.add_field(
                                                            name="Age:", value=results["age"])
                                                        pEmbed.add_field(
                                                            name="Gender:", value=results["gender"])
                                                        pEmbed.add_field(
                                                            name="Interests:", value=results["interests"], inline=False)
                                                        if results['gender'].lower() == "female" or results['gender'].lower() == "girl":
                                                            pEmbed.set_thumbnail(url=girlAV[results['avatar']])

                                                        await thre.send("Preview:", embed = pEmbed, view=cycleButton())
                                                    else: #non-binary
                                                        value = randint(0, 0xffffff)
                                                        pEmbed= discord.Embed(color = value)
                                                        pEmbed.set_author(
                                                            name="Profile")
                                                        pEmbed.add_field(
                                                            name="Age:", value=results["age"])
                                                        pEmbed.add_field(
                                                            name="Gender:", value=results["gender"])
                                                        pEmbed.add_field(
                                                            name="Interests:", value=results["interests"], inline=False)
                                                        pEmbed.set_thumbnail(url=otherAV[results['avatar']])

                                                        await thre.send("Preview:", embed = pEmbed, view=cycleButton())                             
                            except: 
                                user_a = member

                                categ = discord.utils.get(guild.categories, name="PRIVATE SPACE (5)")
                                text_channel = await categ.create_text_channel(f"{member.name}s - {member.discriminator}")
                                await text_channel.set_permissions(user_a, send_messages=True, view_channel=True)
                                await text_channel.set_permissions(guild.default_role, send_messages=False, view_channel=False)
                                await text_channel.edit(topic=f"Custom PRIVATE channel for {member.name}")
                                await text_channel.edit(slowmode_delay=7200)

                                ema = discord.Embed(
                                    description="Please access the `thread channel` to post your profile!"
                                )
                                a = await text_channel.send(f"Welcome {member.mention}!  (≧◡≦)", embed=ema)
                                thre = await text_channel.create_thread(name=f"Intro - {member.name}", message=a, auto_archive_duration=1440, reason=None)

                                if collection.find_one({"_id": member.id}):
                                    await thre.send('Your Intro has already been posted! Type `.intro` to update your old intro.')
                                else: 
                                    def check_join(msg):
                                        return msg.author == member

                                    await thre.send("What is your gender? [Male, Female, Non-Binary]")

                                    try:
                                        msg2 = await self.bot.wait_for("message", check=check_join, timeout=300)
                                    except asyncio.TimeoutError:
                                        error3 = await thre.send("<:disagree:943603027854626816> Introduction process failed")
                                        await asyncio.sleep(5)
                                        await error3.delete()
                                        return

                                    if msg2: 
                                        await thre.send('What is your sexuality?')

                                        try:
                                            msg1 = await self.bot.wait_for("message", check=check_join, timeout=300)
                                        except asyncio.TimeoutError:
                                            error5 = await thre.send("<:disagree:943603027854626816> Introduction process failed")
                                            await asyncio.sleep(5)
                                            await error5.delete()
                                            return
                                        if msg1:
                                            await thre.send("How old are you?")

                                            try:
                                                msg3 = await self.bot.wait_for("message", check=check_join, timeout=300)
                                            except asyncio.TimeoutError:
                                                error5 = await thre.send("<:disagree:943603027854626816> Introduction process failed")
                                                await asyncio.sleep(5)
                                                await error5.delete()
                                                return

                                            if msg3:
                                                await thre.send("Alright last question. What are your interests?")

                                                try:
                                                    msg6 = await self.bot.wait_for("message", check=check_join, timeout=300)
                                                except asyncio.TimeoutError:
                                                    error8 = await thre.send("<:disagree:943603027854626816> Introduction process failed")
                                                    await asyncio.sleep(5)
                                                    await error8.delete()
                                                    return

                                                if msg6:
                                                    writeDocument = 0
                                                    post = {"_id": member.id, "ident": "dating-vent", "avatar": writeDocument, "name": member.name,
                                                            "age": msg3.content, "gender": msg2.content, "interests": msg6.content}
                                                    if collection.find_one({"_id": member.id}):
                                                        collection.update_many({"_id": member.id}, {"$set": {"avatar": writeDocument, "name": member.name,
                                                            "age": msg3.content, "gender": msg2.content, "interests": msg6.content}})
                                                    else:
                                                        collection.insert_one(post)

                                                    results = collection.find_one({"_id": member.id})

                                                    # Setting embed color
                                                    if results['gender'].lower() == "male" or results['gender'].lower() == "boy":
                                                        value = 0x00caff
                                                        pEmbed= discord.Embed(color = value)
                                                        pEmbed.set_author(
                                                            name="Profile")
                                                        pEmbed.add_field(
                                                            name="Age:", value=results["age"])
                                                        pEmbed.add_field(
                                                            name="Gender:", value=results["gender"])
                                                        pEmbed.add_field(
                                                            name="Interests:", value=results["interests"], inline=False)
                                                        if results['gender'].lower() == "male" or results['gender'].lower() == "boy":
                                                            pEmbed.set_thumbnail(url=boyAV[results['avatar']])

                                                        await thre.send("Preview:", embed = pEmbed, view=cycleButton())

                                                    elif results['gender'].lower() == "female" or results['gender'].lower() == 'girl':
                                                        value = 0xff95ff
                                                        pEmbed= discord.Embed(color = value)
                                                        pEmbed.set_author(
                                                            name="Profile")
                                                        pEmbed.add_field(
                                                            name="Age:", value=results["age"])
                                                        pEmbed.add_field(
                                                            name="Gender:", value=results["gender"])
                                                        pEmbed.add_field(
                                                            name="Interests:", value=results["interests"], inline=False)
                                                        if results['gender'].lower() == "female" or results['gender'].lower() == "girl":
                                                            pEmbed.set_thumbnail(url=girlAV[results['avatar']])

                                                        await thre.send("Preview:", embed = pEmbed, view=cycleButton())
                                                    else: #non-binary
                                                        value = randint(0, 0xffffff)
                                                        pEmbed= discord.Embed(color = value)
                                                        pEmbed.set_author(
                                                            name="Profile")
                                                        pEmbed.add_field(
                                                            name="Age:", value=results["age"])
                                                        pEmbed.add_field(
                                                            name="Gender:", value=results["gender"])
                                                        pEmbed.add_field(
                                                            name="Interests:", value=results["interests"], inline=False)
                                                        pEmbed.set_thumbnail(url=otherAV[results['avatar']])

                                                        await thre.send("Preview:", embed = pEmbed, view=cycleButton())
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.guild.id == 999682901308342342:
            guild = self.bot.get_guild(999682901308342342)
            try: 
                memberName = f"{member.name}".lower()
                modifiedName = ''.join(char for char in memberName if char.isalnum() or char in " ").replace(" ", "-")
                channel = discord.utils.get(guild.channels, name=f'{modifiedName}s-{member.discriminator}')
                await channel.delete()
                collection.delete_many({'author_id': member.id})
            except: 
                memberName = f"{member.name}".lower()
                channel = discord.utils.get(guild.channels, name=f'{memberName}s-{member.discriminator}')
                await channel.delete()
                collection.delete_many({'author_id': member.id})
            if collection.find_one({"_id": member.id}):
                existing_data = collection.find_one({"_id": member.id})
                collection.delete_one({"_id": member.id})
                # Delete from General channel
                channel = self.bot.get_channel(999682901786505336)
                txt = await channel.fetch_message(existing_data["msg_id"])
                await txt.delete()

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        if before.avatar != after.avatar:
            if collection.find_one({"_id": before.id}):
                writeDocument = str(after.avatar.url)
                find_before = collection.find_one({"_id": before.id})

                collection.update_one({"_id": before.id}, {
                                      "$set": {"avatar": writeDocument}})
                find_after = collection.find_one({"_id": after.id})

                value = random.randint(0, 0xffffff)
                embed = discord.Embed(color=value)
                embed.set_author(
                    name=find_after["username"], icon_url=find_after["avatar"])
                embed.add_field(name="Age:", value=find_after["age"])
                embed.add_field(name="Gender:", value=find_after["gender"])
                embed.add_field(name="Pronouns:",
                                value=find_after["pronoun"], inline=False)
                embed.add_field(name="Location:",
                                value=find_after["location"], inline=False)
                embed.add_field(name="Interests:",
                                value=find_after["interests"], inline=False)
                embed.set_thumbnail(url=find_after["avatar"])

                channel = self.bot.get_channel(999682901786505336)
                txt = await channel.fetch_message(find_before["msg_id"])
                await txt.edit(embed=embed)
            else:
                return

    @commands.command()
    async def intro(self, ctx):
        cu = ctx.message.author
        if not isinstance(ctx.message.channel, discord.Thread):
            x = await ctx.send("You cannot use that command here! Please go to your `thread channel`")
            await asyncio.sleep(10)
            await ctx.message.delete()
            await x.delete()
        else:
            if collection.find_one({"_id": ctx.author.id}):
                await ctx.send(f"**Your Introduction is already recorded.** Do you want to edit it? [yes/no]")

                def check(msg):
                    return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["y", "Y", "yes", "Yes", "YES", "n", "N", "no", "No", "NO"]

                try:
                    msg = await self.bot.wait_for("message", check=check, timeout=300)
                except asyncio.TimeoutError:
                    error = await ctx.send(f"<:disagree:943603027854626816>  Introduction process failed {cu.mention}")
                    await asyncio.sleep(5)
                    await error.delete()
                    return

                if msg.content.lower() == "y" or msg.content.lower() == "yes":
                    await ctx.send(f"What is your gender? [Male, Female, Non-Binary]")

                    def check3(msg):
                        return msg.author == ctx.author and msg.channel == ctx.channel

                    try:
                        msg3 = await self.bot.wait_for("message", check=check3, timeout=300)
                    except asyncio.TimeoutError:
                        error5 = await ctx.send(f"<:disagree:943603027854626816> Introduction process failed {cu.mention}")
                        await asyncio.sleep(5)
                        await error5.delete()
                        return

                    if msg3: 
                        await ctx.send('What is your sexuality?')

                        try:
                            msg1 = await self.bot.wait_for("message", check=check3, timeout=300)
                        except asyncio.TimeoutError:
                            error5 = await ctx.send("<:disagree:943603027854626816> Introduction process failed")
                            await asyncio.sleep(5)
                            await error5.delete()
                            return
                    if msg1:
                        await ctx.send("How old are you?")

                        try:
                            msg2 = await self.bot.wait_for("message", check=check3, timeout=300)
                        except asyncio.TimeoutError:
                            error5 = await ctx.send("<:disagree:943603027854626816> Introduction process failed")
                            await asyncio.sleep(5)
                            await error5.delete()
                            return
                    if msg2:
                        await ctx.send(f"Alright last question. What are your interests?")

                        def check6(msg):
                            return msg.author == ctx.author and msg.channel == ctx.channel

                        try:
                            msg6 = await self.bot.wait_for("message", check=check6, timeout=300)
                        except asyncio.TimeoutError:
                            error8 = await ctx.send(f"<:disagree:943603027854626816> Introduction process failed {cu.mention}")
                            await asyncio.sleep(5)
                            await error8.delete()
                            return

                    if msg6:
                        pass
                else:
                    await ctx.send(f"Alright sure, have a nice day!")
                    return 

                writeDocument = 0
                post = {"_id": ctx.author.id, "ident": "dating-vent", "avatar": writeDocument, "name": ctx.author.name,
                        "age": msg2.content, "gender": msg3.content, "sexuality": msg1.content, "interests": msg6.content}
                if collection.find_one({"_id": ctx.author.id}):
                    collection.update_many({"_id": ctx.author.id}, {"$set": {"avatar": writeDocument, "name": ctx.author.name,
                        "age": msg2.content, "gender": msg3.content, "sexuality": msg1.content, "interests": msg6.content}})
                else:
                    collection.insert_one(post)

                results = collection.find_one({"_id": ctx.author.id})

                # Setting embed color
                if results['gender'].lower() == "male" or results['gender'].lower() == "boy":
                    value = 0x00caff
                    pEmbed= discord.Embed(color = value)
                    pEmbed.set_author(
                        name="Profile")
                    pEmbed.add_field(
                        name="Age:", value=results["age"])
                    pEmbed.add_field(
                        name="Gender:", value=results["gender"])
                    pEmbed.add_field(
                        name="Sexuality:", value=results["sexuality"])
                    pEmbed.add_field(
                        name="Interests:", value=results["interests"], inline=False)
                    if results['gender'].lower() == "male" or results['gender'].lower() == "boy":
                        pEmbed.set_thumbnail(url=boyAV[results['avatar']])

                    await ctx.channel.send("Preview:", embed = pEmbed, view=cycleButton())

                elif results['gender'].lower() == "female" or results['gender'].lower() == 'girl':
                    value = 0xff95ff
                    pEmbed= discord.Embed(color = value)
                    pEmbed.set_author(
                        name="Profile")
                    pEmbed.add_field(
                        name="Age:", value=results["age"])
                    pEmbed.add_field(
                        name="Gender:", value=results["gender"])
                    pEmbed.add_field(
                        name="Sexuality:", value=results["sexuality"])
                    pEmbed.add_field(
                        name="Interests:", value=results["interests"], inline=False)
                    if results['gender'].lower() == "female" or results['gender'].lower() == "girl":
                        pEmbed.set_thumbnail(url=girlAV[results['avatar']])

                    await ctx.channel.send("Preview:", embed = pEmbed, view=cycleButton())
                else: #non-binary
                    existing_data = collection.find_one({"_id": ctx.author.id})
                    value = randint(0, 0xffffff)
                    pEmbed= discord.Embed(color = value)
                    pEmbed.set_author(
                        name="Profile")
                    pEmbed.add_field(
                        name="Age:", value=results["age"])
                    pEmbed.add_field(
                        name="Gender:", value=results["gender"])
                    pEmbed.add_field(
                        name="Sexuality:", value=results["sexuality"])
                    pEmbed.add_field(
                        name="Interests:", value=results["interests"], inline=False)
                    pEmbed.set_thumbnail(url=otherAV[results['avatar']])

                    await ctx.channel.send("Preview:", embed = pEmbed, view=cycleButton())
                # writeDocument = str(ctx.author.avatar.url)

                # existing_data = collection.find_one(
                #     {"_id": ctx.author.id})

                # collection.update_many({"_id": ctx.author.id}, {"$set": {"avatar": writeDocument,
                #                        "age": msg2.content, "gender": msg3.content, "interests": msg6.content}})

                # results = collection.find_one({"_id": ctx.author.id})

                # # Setting embed color
                # if results['gender'].lower() == "male" or results['gender'].lower() == "boy":
                #     value = 0x00caff
                # elif results['gender'].lower() == "female" or results['gender'].lower() == 'girl':
                #     value = 0xff95ff
                # else: 
                #     value = random.randint(0, 0xffffff)

                # embed = discord.Embed(color=value)
                # embed.set_author(
                #     name="Profile", icon_url=ctx.author.guild.icon)
                # embed.add_field(
                #     name="Age:", value=results["age"])
                # embed.add_field(
                #     name="Gender:", value=results["gender"])
                # embed.add_field(
                #     name="Interests:", value=results["interests"], inline=False)
                # embed.set_thumbnail(
                #     url=results["avatar"])
                # channel = self.bot.get_channel(999682901786505336)
                # txt = await channel.fetch_message(existing_data["msg_id"])
                # await txt.edit(embed=embed)

                # collection.update_one({"_id": ctx.author.id}, {
                #                       "$set": {"msg_id": txt.id}})

            else:
                await ctx.send(f"Shall we start? [yes/no]")

                def check(msg):
                    return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["y", "Y", "yes", "Yes", "YES", "n", "N", "no", "No", "NO"]

                try:
                    msg = await self.bot.wait_for("message", check=check, timeout=300)
                except asyncio.TimeoutError:
                    error = await ctx.send(f"<:disagree:943603027854626816> Introduction process failed {cu.mention}")
                    await asyncio.sleep(5)
                    await error.delete()
                    return

                if msg.content.lower() == "y" or msg.content.lower() == "yes" :
                    await ctx.send(f"What is your gender? [Male, Female, Non-Binary]")

                    def check3(msg):
                        return msg.author == ctx.author and msg.channel == ctx.channel

                    try:
                        msg3 = await self.bot.wait_for("message", check=check3, timeout=300)
                    except asyncio.TimeoutError:
                        error5 = await ctx.send(f"<:disagree:943603027854626816> Introduction process failed {cu.mention}")
                        await asyncio.sleep(5)
                        await error5.delete()
                        return
                    
                    if msg3: 
                        await ctx.send('What is your sexuality?')

                        try:
                            msg1 = await self.bot.wait_for("message", check=check3, timeout=300)
                        except asyncio.TimeoutError:
                            error5 = await ctx.send("<:disagree:943603027854626816> Introduction process failed")
                            await asyncio.sleep(5)
                            await error5.delete()
                            return
                    if msg1:
                        await ctx.send("How old are you?")

                        try:
                            msg2 = await self.bot.wait_for("message", check=check3, timeout=300)
                        except asyncio.TimeoutError:
                            error5 = await ctx.send("<:disagree:943603027854626816> Introduction process failed")
                            await asyncio.sleep(5)
                            await error5.delete()
                            return
                    if msg2:
                        await ctx.send(f"Alright last question. What are your interests?")

                        def check6(msg):
                            return msg.author == ctx.author and msg.channel == ctx.channel

                        try:
                            msg6 = await self.bot.wait_for("message", check=check6, timeout=300)
                        except asyncio.TimeoutError:
                            error8 = await ctx.send(f"<:disagree:943603027854626816> Introduction process failed {cu.mention}")
                            await asyncio.sleep(5)
                            await error8.delete()
                            return

                    if msg6:
                        pass
                else:
                    await ctx.send(f"Alright sure, have a nice day!")
                    return

                writeDocument = 0
                post = {"_id": ctx.author.id, "ident": "dating-vent", "avatar": writeDocument, "name": ctx.author.name,
                        "age": msg2.content, "gender": msg3.content, "sexuality": msg1.content, "interests": msg6.content}
                if collection.find_one({"_id": ctx.author.id}):
                    collection.update_many({"_id": ctx.author.id}, {"$set": {"avatar": writeDocument, "name": ctx.author.name,
                        "age": msg2.content, "gender": msg3.content, "sexuality": msg1.content, "interests": msg6.content}})
                else:
                    collection.insert_one(post)

                results = collection.find_one({"_id": ctx.author.id})

                # Setting embed color
                if results['gender'].lower() == "male" or results['gender'].lower() == "boy":
                    value = 0x00caff
                    pEmbed= discord.Embed(color = value)
                    pEmbed.set_author(
                        name="Profile")
                    pEmbed.add_field(
                        name="Age:", value=results["age"])
                    pEmbed.add_field(
                        name="Gender:", value=results["gender"])
                    pEmbed.add_field(
                        name="Sexuality:", value=results["sexuality"])
                    pEmbed.add_field(
                        name="Interests:", value=results["interests"], inline=False)
                    if results['gender'].lower() == "male" or results['gender'].lower() == "boy":
                        pEmbed.set_thumbnail(url=boyAV[results['avatar']])

                    await ctx.channel.send("Preview:", embed = pEmbed, view=cycleButton())

                elif results['gender'].lower() == "female" or results['gender'].lower() == 'girl':
                    value = 0xff95ff
                    pEmbed= discord.Embed(color = value)
                    pEmbed.set_author(
                        name="Profile")
                    pEmbed.add_field(
                        name="Age:", value=results["age"])
                    pEmbed.add_field(
                        name="Gender:", value=results["gender"])
                    pEmbed.add_field(
                        name="Sexuality:", value=results["sexuality"])
                    pEmbed.add_field(
                        name="Interests:", value=results["interests"], inline=False)
                    if results['gender'].lower() == "female" or results['gender'].lower() == "girl":
                        pEmbed.set_thumbnail(url=girlAV[results['avatar']])

                    await ctx.channel.send("Preview:", embed = pEmbed, view=cycleButton())
                else: #non-binary
                    existing_data = collection.find_one({"_id": ctx.author.id})
                    value = randint(0, 0xffffff)
                    pEmbed= discord.Embed(color = value)
                    pEmbed.set_author(
                        name="Profile")
                    pEmbed.add_field(
                        name="Age:", value=results["age"])
                    pEmbed.add_field(
                        name="Gender:", value=results["gender"])
                    pEmbed.add_field(
                        name="Sexuality:", value=results["sexuality"])
                    pEmbed.add_field(
                        name="Interests:", value=results["interests"], inline=False)
                    pEmbed.set_thumbnail(url=otherAV[results['avatar']])

                    await ctx.channel.send("Preview:", embed = pEmbed, view=cycleButton())
                # writeDocument = str(ctx.author.avatar.url)
                # post = {"_id": ctx.author.id, "ident": "cb", "avatar": writeDocument, "name": ctx.author.name, "age": msg2.content, "gender": msg3.content, "interests": msg6.content}

                # if collection.find_one({"_id": ctx.author.id}):
                #     collection.update_many({"_id": ctx.author.id}, {"$set": {"avatar": writeDocument,  "name": ctx.author.name, "age": msg2.content, "gender": msg3.content, "interests": msg6.content}})
                # else:
                #     collection.insert_one(post)

                # results = collection.find_one({"_id": ctx.author.id})

                # # Setting embed color
                # if results['gender'].lower() == "male" or results['gender'].lower() == "boy":
                #     value = 0x00caff
                # elif results['gender'].lower() == "female" or results['gender'].lower() == 'girl':
                #     value = 0xff95ff
                # else: 
                #     value = random.randint(0, 0xffffff)

                # embed = discord.Embed(color=value)
                # embed.set_author(
                #     name="Profile", icon_url=ctx.author.guild.icon)
                # embed.add_field(
                #     name="Age:", value=results["age"])
                # embed.add_field(
                #     name="Gender:", value=results["gender"])
                # embed.add_field(
                #     name="Interests:", value=results["interests"], inline=False)
                # embed.set_thumbnail(
                #     url=results["avatar"])
                # a = self.bot.get_channel(999682901786505336)
                # xx = await a.send(embed=embed)
                # await xx.add_reaction("💌")

                # collection.update_one({"_id": ctx.author.id}, {
                #                       "$set": {"msg_id": xx.id}})
    @commands.command()
    async def bin(self, ctx):
        if ctx.channel.category.name == "💌 INBOX":
            topic = ctx.channel.topic
            topicID = ""
            for i, v in enumerate(topic):
                if v in "0123456789":
                    topicID += v
            print(topicID)
            guild = self.bot.get_guild(999682901308342342)
            other_chn = guild.get_channel(int(topicID))

            #Deleting data from DB 
            inbox.delete_one({"channel":f"{ctx.channel.name}".upper()})
            # try: 
            #     inbox.delete_one({"reactor": int(ctx.message.author.id)})
            # except: 
            #     inbox.delete_one({"author": int(ctx.message.author.id)})

            await ctx.send("Deleting the channel in 10 seconds!")
            await asyncio.sleep(10)
            await ctx.channel.delete()
            await other_chn.delete()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.guild_id == 999682901308342342:
            if not payload.member.bot:
                if payload.emoji.name == "💌":
                    # Check if reaction user profile is already in db or not
                    if not collection.find_one({'_id': payload.member.id}):
                        channel = self.bot.get_channel(payload.channel_id)
                        message = channel.get_partial_message(payload.message_id)
                        try: 
                            await message.remove_reaction(payload.emoji ,payload.member)
                            await payload.member.send("You need to upload your profile first!")
                        except:
                            await message.remove_reaction(payload.emoji ,payload.member)
                    else: 
                        channel = self.bot.get_channel(payload.channel_id)
                        message = channel.get_partial_message(payload.message_id)
                        await message.remove_reaction(payload.emoji ,payload.member)
                        if collection.find_one({"msg_id": payload.message_id}):
                            db_data = collection.find_one({"msg_id": payload.message_id})
                            guild = self.bot.get_guild(payload.guild_id)
                            user_a = payload.member
                            server = self.bot.get_guild(999682901308342342)
                            msg_owner = server.get_member(db_data["_id"])
                            if msg_owner is None: 
                                await user_a.send("Profile owner not found! They probably left the server.")
                            else:
                                characters = '1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
                                inboxCode = "".join(choice(characters)
                                                for x in range(randint(2, 5)))

                                categOwner = discord.utils.get(guild.categories, name="💌 INBOX")

                                text_channel_replier = await categOwner.create_text_channel(f"{inboxCode}")

                                await text_channel_replier.set_permissions(user_a, send_messages=True, view_channel=True)
                                await text_channel_replier.set_permissions(msg_owner, view_channel=False)
                                await text_channel_replier.set_permissions(guild.default_role, send_messages=False, view_channel=False)
                                binEmbed = discord.Embed(description="Use `.bin` command here to close this inbox", colour=discord.Colour.red())
                                await text_channel_replier.send(f"You can send your message here and it will be sent to them automatically! <@{payload.member.id}>", embed = binEmbed)

                                results = collection.find_one({"_id": int(db_data["_id"])})

                                if results['gender'] == "male" or results['gender'] == 'boy' or results['gender'] == 'man':
                                    value = 0x00caff
                                elif results['gender'] == "female" or results['gender'] == 'girl' or results['gender'] == 'woman':
                                    value = 0xff95ff
                                else:
                                    value = randint(0, 0xffffff)

                                if collection.find_one({"_id": int(db_data["_id"])}):  
                                    embed= discord.Embed(color = value)
                                    embed.set_author(
                                        name="Profile")
                                    embed.add_field(
                                        name="Age:", value=results["age"])
                                    embed.add_field(
                                        name="Gender:", value=results["gender"])
                                    embed.add_field(
                                            name="Sexuality:", value=results["sexuality"])
                                    embed.add_field(
                                        name="Interests:", value=results["interests"], inline=False)
                                    embed.set_thumbnail(url=results['avatarURL'])
                                await text_channel_replier.send(embed=embed)

                                text_channel_owner = await categOwner.create_text_channel(f"{inboxCode}")

                                await text_channel_owner.set_permissions(user_a, view_channel=False)
                                await text_channel_owner.set_permissions(msg_owner, send_messages=True, view_channel=True)
                                await text_channel_owner.set_permissions(guild.default_role, send_messages=False, view_channel=False)
                                await text_channel_owner.edit(topic=f"{str(text_channel_replier.id)}")
                                await text_channel_replier.edit(topic=f"{str(text_channel_owner.id)}")
                                #await text_channel_owner.send(f"Someone wants to talk to you about {db_data['msg_link']}. You'll recieve their message here and you can reply to it by texting here. <@{db_data['_id']}>", embed = binEmbed)

                                await text_channel_owner.send(f"Someone is interested in you. You'll recieve their message here and you can reply to it by texting here. <@{db_data['_id']}>", embed=binEmbed)

                                results = collection.find_one({"_id": payload.member.id})

                                if results['gender'] == "male" or results['gender'] == 'boy' or results['gender'] == 'man':
                                    value = 0x00caff
                                elif results['gender'] == "female" or results['gender'] == 'girl' or results['gender'] == 'woman':
                                    value = 0xff95ff
                                else:
                                    value = randint(0, 0xffffff)

                                if collection.find_one({"_id": payload.member.id}):  
                                    embed= discord.Embed(color = value)
                                    embed.set_author(
                                        name="Profile")
                                    embed.add_field(
                                        name="Age:", value=results["age"])
                                    embed.add_field(
                                        name="Gender:", value=results["gender"])
                                    embed.add_field(
                                            name="Sexuality:", value=results["sexuality"])
                                    embed.add_field(
                                        name="Interests:", value=results["interests"], inline=False)
                                    embed.set_thumbnail(url=results['avatarURL'])
                                await text_channel_owner.send(embed=embed)
                                
                                # Inserting Inbox information in the DataBase
                                post={"channel":f"{inboxCode}", "reactor":payload.member.id, "author":int(db_data["_id"])}
                                inbox.insert_one(post)

                        else:
                            print('Cannot find message id in DataBase!')
                            await payload.member.send('Profile owner probably left the server!')

    @commands.Cog.listener()
    async def on_message(self, msg): 
        if not msg.guild:
            return
        if msg.guild.id == 999682901308342342:
            if msg.channel.category is not None:
                if msg.channel.category.id == 1000038353854533773: #is triggered only in inbox channels 
                    if not msg.author.bot:
                        if msg.content.startswith("."):
                            pass
                        else:
                            if "REPORTED" in msg.channel.topic:
                                await msg.add_reaction("<:disagree:943603027854626816>")
                            elif "Reporter" in msg.channel.topic:
                                print("Reporter channel detected")
                            else:
                                topic = msg.channel.topic
                                
                                msgContent = msg.content
                                chn = msg.guild.get_channel(int(topic))
                                em = discord.Embed(
                                    description=msg.content
                                )
                                em.set_author(
                                    name="Stranger", icon_url="https://image.similarpng.com/very-thumbnail/2020/08/Emoji-social-media-Reaction-heart-icon-vector-PNG.png")
                                x = await chn.send(embed=em, view=repButton())
                                await msg.add_reaction("<:agree:943603027313565757>")
            
            #Global Chat 
            if not msg.author.bot:
                if msg.channel.category.id == 999927005179035738: 
                    if collection.find_one({"_id": msg.author.id}):
                        if gChat.find_one({"_id": msg.author.id}):
                            data = gChat.find_one({"_id": msg.author.id})
                            if data['ident'] == 0:
                                return
                            else: 
                                post1 = {"lastmessage": msg.author.id}
                                his = dHistory.find_one({"lastmessage": msg.author.id})
                                globalChannel = msg.guild.get_channel(1000989536861560862)
                                try: 
                                    if not his['lastmessage'] == msg.author.id: 
                                        await globalChannel.send(f'{data["username"]}```{msg.content}```')
                                    else: 
                                        await globalChannel.send(f"```{msg.content}```")
                                        dHistory.delete_many({})
                                except: 
                                        await globalChannel.send(f'{data["username"]}```{msg.content}```')
                                        dHistory.delete_many({})
                                dHistory.insert_one(post1)

                        else:
                            post = {"_id": msg.author.id, 'username': "-", 'ident': 0}
                            gChat.insert_one(post)
                            await msg.channel.send(f"What will be your `display name`?")

                            def check(msg):
                                return msg.author == msg.author and msg.channel == msg.channel and msg.guild.id == 999682901308342342

                            try:
                                msg1 = await self.bot.wait_for("message", check=check, timeout=300)
                            except asyncio.TimeoutError:
                                error5 = await msg.channel.send(f"<:disagree:943603027854626816> TimedOut {msg.author.mention}")
                                await asyncio.sleep(5)
                                await error5.delete()
                                return
                            pass
                            if msg1: 
                                gChat.update_one({"_id":msg.author.id}, {"$set":{"username":msg1.content}})
                                gChat.update_one({"_id": msg.author.id}, {"$inc": {"ident": 1}})
                                await msg.channel.send('Now you can start chatting :)')
                            
            

async def setup(bot):
    await bot.add_cog(dating(bot))