#pylint: disable=unused-variable

import discord
import Databases.sparked_db as sparked_db
import fwgconfig
from random import randrange
import aiohttp
import emoji
from discord.ext import commands
from discord.ui import Button, View, Modal, InputText
from discord.utils import find

class DetModal(Modal): #Money lost or data loss help
    def __init__(self, bot, *args, **kwargs):
        self.bot = bot
        super().__init__(*args,**kwargs)

        self.add_item(InputText(
            label= "How much data did you lose?",
            placeholder= "I lost all of my data / I lost some of my data",
            style=discord.InputTextStyle.short,
            max_length=400
        ))

        self.add_item(InputText(
            label= "For which game did you lose your data?",
            placeholder= "Airport Tycoon / Prison Tycoon",
            style=discord.InputTextStyle.short,
            max_length=400
        ))

        self.add_item(InputText(
            label= "What data did you lose?",
            placeholder= "Cash / Tycoon / Both / Other (Specify)",
            style=discord.InputTextStyle.short,
            max_length=400
        ))

        self.add_item(InputText(
            label= "Did you get disconnected by any chance?",
            placeholder= "Yes / No",
            style=discord.InputTextStyle.short,
            max_length=5
        ))

        self.add_item(InputText(
            label= "How much did you lose?",
            placeholder= "10 million... Specify.",
            style=discord.InputTextStyle.short,
            max_length=400
        ))

    async def callback(self, interaction:discord.Interaction):
        embed = discord.Embed(title=f"Support has finished.", color=0xFFFFFF)
        embed.add_field(name="Variables:", value=f"**User:** {interaction.user.mention}\n**How much data lost:** {self.children[0].value}\n**Game data loss:** {self.children[1].value}\n**Data lost:** {self.children[2].value}\n**Disconnected?:** {self.children[3].value}\n**Quantity lost: **{self.children[4].value}", inline=False)

        sendc = self.bot.get_channel(1028804301205807154) #uses support-answers channel
        await sendc.send(embed=embed)
        await interaction.response.send_message('Thanks for submitting! We will be right back with you soon.', ephemeral=True)

class PurModel(Modal): #Purchase Help
    def __init__(self, bot, *args, **kwargs):
        self.bot = bot
        super().__init__(*args,**kwargs)

        self.add_item(InputText(
            label= "What Item did you buy?",
            placeholder= "A VIP Pass...",
            style=discord.InputTextStyle.short,
            max_length=400
        ))

        self.add_item(InputText(
            label= "Did you receive your item?",
            placeholder= "Yes / No",
            style=discord.InputTextStyle.short,
            max_length=5
        ))

        self.add_item(InputText(
            label= "What happened to your purchase?",
            placeholder= "I didn't get it because... ",
            style=discord.InputTextStyle.long,
            min_length=400
        ))

    async def callback(self, interaction:discord.Interaction):
        embed = discord.Embed(title=f"Support has finished.", color=0xFFFFFF)
        embed.add_field(name="Variables:", value=f"**User:** {interaction.user.mention}\n**Item bought:** {self.children[0].value}\n**Item received:** {self.children[1].value}\n**Reason for help:** {self.children[2].value}", inline=False)

        sendc = self.bot.get_channel(926180074854682694)
        await sendc.send(embed=embed)
        await interaction.response.send_message('Thanks for submitting! We will be right back with you soon.', ephemeral=True)

class SecModel(Modal): #Discord Help
    def __init__(self, bot, *args, **kwargs):
        self.bot = bot
        super().__init__(*args,**kwargs)

        self.add_item(InputText(
            label= "Describe your problem here",
            placeholder= "I can't upload images...",
            style=discord.InputTextStyle.long,
            min_length=400
        ))

        self.add_item(InputText(
            label= "Is this related to moderating?",
            placeholder= "Yes / No",
            style=discord.InputTextStyle.short,
            max_length=5
        ))

        self.add_item(InputText(
            label= "Provide the approx. date of the problem",
            placeholder= "Around Oct. 5 at 15:00...",
            style=discord.InputTextStyle.long,
            min_length=8,
            max_length=400
        ))

    async def callback(self, interaction:discord.Interaction):
        embed = discord.Embed(title=f"Support has finished.", color=0xFFFFFF)
        embed.add_field(name="Variables:", value=f"**User:** {interaction.user.mention}\n**Problem Desc:** {self.children[0].value}\n**Mod Related:** {self.children[1].value}\n**Aprox Date:** {self.children[2].value}", inline=False)

        sendc = self.bot.get_channel(926180074854682694)
        await sendc.send(embed=embed)
        await interaction.response.send_message('Thanks for submitting! We will be right back with you soon.', ephemeral=True)

class OthModel(Modal): #Other Help
    def __init__(self, bot, *args, **kwargs):
        self.bot = bot
        super().__init__(*args,**kwargs)

        self.add_item(InputText(
            label= "Describe your problem here",
            placeholder= "I can't upload images...",
            style=discord.InputTextStyle.long,
            min_length=50
        ))

        self.add_item(InputText(
            label= "Is this related to moderating?",
            placeholder= "Yes / No",
            style=discord.InputTextStyle.short,
            max_length=5
        ))

        self.add_item(InputText(
            label= "Provide the approx. date of the problem",
            placeholder= "Around Oct. 5 at 15:00...",
            style=discord.InputTextStyle.long,
            min_length=8,
            max_length=400
        ))

    async def callback(self, interaction:discord.Interaction):
        embed = discord.Embed(title=f"Support has finished.", color=0xFFFFFF)
        embed.add_field(name="Variables:", value=f"**User:** {interaction.user.mention}\n**Problem Desc:** {self.children[0].value}\n**Mod Related:** {self.children[1].value}\n**Aprox Date:** {self.children[2].value}", inline=False)

        sendc = self.bot.get_channel(926180074854682694)
        await sendc.send(embed=embed)
        await interaction.response.send_message('Thanks for submitting! We will be right back with you soon.', ephemeral=True)


class MyView(View):

    def __init__(self, bot):
        
        self.bot = bot
        super().__init__()

    @discord.ui.button(label= "Your Game Data", style=discord.ButtonStyle.blurple, custom_id="gdata")
    async def button_callback(self, button, interaction):
        msgid = interaction.message.id
        idlist = ["gdata","ipurch","disc","othr","canc"]
        for ids in idlist:
            b = [x for x in self.children if x.custom_id == ids][0]
            b.disabled = True
        modal = DetModal(title="Game Data Form Help",bot=self.bot)
        await interaction.response.send_modal(modal)
        await interaction.followup.edit_message(msgid, view=self)

    @discord.ui.button(label= "An Item Purchase", style=discord.ButtonStyle.blurple, custom_id="ipurch")
    async def button_callback2(self, button, interaction):
        msgid = interaction.message.id
        idlist = ["gdata","ipurch","disc","othr","canc"]
        for ids in idlist:
            b = [x for x in self.children if x.custom_id == ids][0]
            b.disabled = True
        
        modal = PurModel(title="Item Purchase Form Help", bot=self.bot)
        await interaction.response.send_modal(modal)
        await interaction.followup.edit_message(msgid, view=self)

    @discord.ui.button(label= "Discord", style=discord.ButtonStyle.blurple, custom_id="disc")
    async def button_callback3(self, button, interaction):
        msgid = interaction.message.id
        idlist = ["gdata","ipurch","disc","othr","canc"]
        for ids in idlist:
            b = [x for x in self.children if x.custom_id == ids][0]
            b.disabled = True
        
        modal = SecModel(title="Discord Form Help", bot=self.bot)
        await interaction.response.send_modal(modal)
        await interaction.followup.edit_message(msgid, view=self)
    
    @discord.ui.button(label= "Other", style=discord.ButtonStyle.blurple, custom_id="othr")
    async def button_callback4(self, button, interaction):
        msgid = interaction.message.id
        idlist = ["gdata","ipurch","disc","othr","canc"]
        for ids in idlist:
            b = [x for x in self.children if x.custom_id == ids][0]
            b.disabled = True
        modal = OthModel(title="Other Form Help", bot=self.bot)
        await interaction.response.send_modal(modal)
        await interaction.followup.edit_message(msgid, view=self)

    @discord.ui.button(label= "Cancel", style=discord.ButtonStyle.blurple, custom_id="canc")
    async def button_callback5(self, button, interaction):
        msgid = interaction.message.id
        idlist = ["gdata","ipurch","disc","othr","canc"]
        for ids in idlist:
            b = [x for x in self.children if x.custom_id == ids][0]
            b.disabled = True
        await interaction.response.send_message("Process Cancelled!", ephemeral=True)
        await interaction.followup.edit_message(msgid, view=self)



class MyMessages(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener("on_member_join")
    async def change_invalid_nick(self, member):
        membero:str = member.name
        if not membero.isascii():
            await member.edit(nick="Change your name")
            await member.send('Please change your nickname. Non ASCII Characters are not allowed.')

    @commands.Cog.listener("on_message")
    async def prevent_post_airlines(self, message):
        if message.channel.id == 1021180575140302902:
            if message.author.bot:
                return
            return await message.delete()
    

    #Tells whoever invites this bot to their server to just... It won't work :P
    @commands.Cog.listener("on_guild_join")
    async def disable_bot_on_join(self, guild):
        try:
            general = find(lambda x:x.name == 'general', guild.text_channels)
            if general and general.permissions_for(guild.me).send_messages:
                await general.send("""Hello {}! Thanks for inviting me to this amazing server, 
                although **every** function has been disabled.\n\n Why? Our bot is only for private usage, 
                if you use it anywhere else rather than the Official [Airplane Simulator](https://discord.gg/xD3x4pVDV6) Or 
                [Fat Whale Games](https://discord.gg/u6gzUEn), 
                it won't work.\n
                You are able to invite this bot for the sole purpose of making it a verified bot! Your help is appreciated.""")
        except Exception:
            pass

    def message_nuller(message) -> bool:
        if (
            message.guild is None
            or message.author.bot
            or message.guild.id not in fwgconfig.fwgguilds #fwgconfig.fwgguilds = list of guilds/
            
            #Below if uncommented will only make message triggers available for use to Florian and Me.
            #or message.author.id not in [348174141121101824,290078194298519552]
        ):
            return False
        else:
            return True

    #THIS CHECKS FOR ATTACHMENTS
    @commands.Cog.listener("on_message")
    async def attachment_checker(self, message):

        #Checks if the bot should/should not answer
        if MyMessages.message_nuller(message):

            #Check if the message has any attachments
            if len(message.attachments) > 0:
                #Message with an WMV Filetype
                if message.attachments[0].url.endswith('wmv'):
                    embed=discord.Embed(title=emoji.emojize("Possible malicious file detected! :shield:"), description=" ", color=0xFF0000)
                    embed.set_author(name=self.bot.user, icon_url=self.bot.user.avatar_url)
                    embed.set_thumbnail(url="https://www.freeiconspng.com/uploads/error-icon-15.png")
                    embed.add_field(name="WMV Files are not allowed on the server:", value=('If you want to send a video, upload it with an **MP4 file**.\nNeed an online converter? Use this: \nhttps://cloudconvert.com/wmv-to-mp4'), inline=False)
                    embed.set_footer(text="This message will be automatically deleted in 180 seconds.")
                    await message.channel.send(embed=embed, delete_after=180.0)
                    return await message.delete()

    @commands.Cog.listener("on_guild_channel_create")
    async def supportbot(self, channel):
            ch:str = channel.name
            if 'ticket' in ch.lower():
                if channel.guild.id is 645052129710571581:
                    view = MyView(bot=self.bot)
                    await channel.send("Hi! It's Fat Whale Bot. What can I help you with?", view=view)

    @commands.Cog.listener("on_message")
    async def minihelp(self, message):
        if 'help' in message.content:
            if message.channel.id is 645052129710571581:
                await message.channel.send("Need help? For general help type /faq (WIP) and for support, create a ticket in <#720322615134257202>") #support channel



    #THIS CHECKS IF THE BOT/STAFF/ETC HAS BEEN PINGED
    @commands.Cog.listener("on_message")
    async def check_for_pings(self, message):

        if MyMessages.message_nuller(message):
            if 5 > randrange(10): return
            if self.bot.user.mentioned_in(message) and message.mention_everyone is False:

                search_url = 'https://zenquotes.io/api/random'
                search_headers = None

                async with aiohttp.ClientSession() as session:
                    async with session.get(search_url, headers=search_headers) as resp:
                        json_resp = await resp.json()
                
                quote_dict = json_resp[0]
                quote_quote = quote_dict['q']
                quote_author = quote_dict['a']
                
                await message.channel.send(f'{quote_quote} - {quote_author}')
                #Whoever desires to ping me... Will face the truthless end.

            else:
                if message.author.id not in sparked_db.operatorlistcheck():
                    for i in sparked_db.operatorlistcheck():
                        didyoupingme = self.bot.get_user(i)
                        #print(didyoupingme) (Print the operator list in didyoupingme)
                        if didyoupingme.mentioned_in(message):
                            #Get Discord User Status
                            mystatus = message.guild.get_member(i)
                            #Execute actions depending on the status of the member
                            if str(mystatus.status) == "offline":
                                await message.channel.send(f'The staff member {didyoupingme.name} is currently offline! Please refrain from pinging them!',  delete_after=25.0)
                            elif str(mystatus.status) == "idle":
                                await message.channel.send(f'The staff member {didyoupingme.name} is currently idle! Please refrain from pinging them!',  delete_after=25.0)
                            elif str(mystatus.status) == "dnd":
                                await message.channel.send(f'The staff member {didyoupingme.name} is currently busy (Do not disturb). Please refrain from pinging them!', delete_after=25.0)

def setup(bot):
    bot.add_cog(MyMessages(bot))