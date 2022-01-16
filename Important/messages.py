#pylint: disable=unused-variable

import discord
import asyncio
import Databases.sparked_db as sparked_db
import fwgconfig
import random
import emoji
from discord.ext import commands
from discord.utils import find

PingBotChoices = fwgconfig.pingbotrandomanswers


class MyMessages(commands.Cog):

    def __init__(self, bot):
        self.bot = bot



    #Tells whoever invites this bot to their server to just... It won't work :P
    @commands.Cog.listener("on_guild_join")
    async def disable_bot_on_join(self, guild):
        try:
            general = find(lambda x:x.name == 'general', guild.text_channels)
            if general and general.permissions_for(guild.me).send_messages:
                await general.send("""Hello {}! Thanks for inviting me to this amazing server, 
                although **every** function has been disabled.\n\n Why? Our bot is only for private usage, 
                if you use it anywhere else rather than the Official [Airplane Simulator](https://discord.gg/xD3x4pVDV6) Discord Server, it won't work.\n
                You are able to invite this bot for the sole purpose of making it a verified bot! Your help is appreciated.""")
        except Exception:
            pass



    #THIS CHECKS FOR ATTACHMENTS
    @commands.Cog.listener("on_message")
    async def attachment_checker(self, message):

        #Checks if the bot should/should not answer
        if (
            message.guild is None
            or message.author.bot
            or message.guild.id != 856678143608094751
            #Below if uncommented will only make commands available for use to Florian and Me.
            #or message.author.id not in [348174141121101824,290078194298519552]
        ):
            return

        #Check if the message has any attachments
        if len(message.attachments) > 0:
            #Message with an WMV Filetype
            ctx = await self.bot.get_context(message)
            if message.attachments[0].url.endswith('wmv'):
                embed=discord.Embed(title=emoji.emojize("Possible malicious file detected! :shield:"), description=" ", color=0xFF0000)
                embed.set_author(name=self.bot.user, icon_url=self.bot.user.avatar_url)
                embed.set_thumbnail(url="https://www.freeiconspng.com/uploads/error-icon-15.png")
                embed.add_field(name="WMV Files are not allowed on the server:", value=('If you want to send a video, upload it with an **MP4 file**.\nNeed an online converter? Use this: \nhttps://cloudconvert.com/wmv-to-mp4'), inline=False)
                embed.set_footer(text="This message will be automatically deleted in 180 seconds.")
                await message.channel.send(embed=embed, delete_after=180.0)
                return await message.delete()

            elif ctx.valid:
                #This was made so the -planesuggest command works correctly (quicksuggest mode)
                await self.bot.process_commands(message)




    #THIS CHECKS FOR ALL COMMANDS LIST
    @commands.Cog.listener("on_message")
    async def command_checker(self, message):
        cmdChannel = self.bot.get_channel(858832574076157993)
        if (
            message.guild is None
            or message.author.bot
            or message.guild.id != 856678143608094751
            #Below if uncommented will only make commands available for use to Florian and Me.
            #or message.author.id not in [348174141121101824,290078194298519552]
        ):
            return

        ctx = await self.bot.get_context(message)
        if ctx.valid:
            if message.author.id in sparked_db.operatorlistcheck():
                #Author is Operator, evading all checks for commands.
                await self.bot.process_commands(message)
            elif message.channel.id == cmdChannel.id:
                #command invoked in command channel - execute it
                await self.bot.process_commands(message)
            else:
                #command attempted in non command channel - redirect user
                await message.channel.send('This command is only allowed in {}!'.format(cmdChannel.mention), delete_after=5.0)
                await asyncio.sleep(3)
                return await message.delete()




    #THIS CHECKS IF THE BOT/STAFF/ETC HAS BEEN PINGED
    @commands.Cog.listener("on_message")
    async def check_for_pings(self, message):
        if (
            message.guild is None
            or message.author.bot
            or message.guild.id != 856678143608094751
            #Below if uncommented will only make commands available for use to Florian and Me.
            #or message.author.id not in [348174141121101824,290078194298519552]
        ):
            return


        if self.bot.user.mentioned_in(message) and message.mention_everyone is False:
            #Whoever desires to ping me... Will face the truthless end.
            await message.channel.send(random.choice(PingBotChoices))

        else:
            for i in sparked_db.operatorlistcheck():
                didyoupingme = self.bot.get_user(i)
                #print(didyoupingme) (Print the operator list in didyoupingme)
                if didyoupingme.mentioned_in(message):
                    #IF USER PINGS HIMSELF AND ITS ON THE OPERATOR LIST
                    ctx = await self.bot.get_context(message)
                    if message.author.id in sparked_db.operatorlistcheck() and ctx.valid:
                        return await self.bot.process_commands(message)
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