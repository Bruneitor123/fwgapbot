#pylint: disable=unused-variable

import discord
import asyncio
import pymysql
#Database Entries and More
import fwgconfig

from DMSupport.dm_embeds import createFAQEmbed, StartSupport, createMSGEmbed, InmediateSupport
from discord.ext import commands, tasks

DB_IP = fwgconfig.DATABASE_IP
DB_USER = fwgconfig.DATABASE_USER
DB_PASS = fwgconfig.DATABASE_PASSWORD
DB_DB = fwgconfig.DATABASE_DATABASE
DB_PORT = int(fwgconfig.DATABASE_PORT)

class DMSupport(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, aliases=["claim", "forceclaim"])
    @commands.has_role('Support')
    async def forcesupport(self, ctx):
        db = pymysql.connect(host=DB_IP,user=DB_USER,password=DB_PASS,database=DB_DB, port=DB_PORT,charset='utf8')
        c = db.cursor()
        checkforchannel = "SELECT channelusinguser FROM dmsupport WHERE `channelusinguser` = '%s'"
        c.execute(checkforchannel, ctx.channel.id)

        checking = c.fetchone()

        try:
            strtoint = int(''.join(map(str, checking)))
        except:
            return await ctx.send("The channel you are trying to use this command is not a ticket!", delete_after=5.0)
        else:
            updateactualstaff = "UPDATE `dmsupport` SET `staffuser_id` = %s WHERE `channelusinguser` = '%s'"
            c.execute(updateactualstaff, (ctx.author.id, ctx.channel.id))
            db.commit()
            return await ctx.send(f'The user {ctx.author.mention} now has control over this ticket!')

    @commands.command(hidden=True)
    @commands.has_role('Support')
    async def close(self, ctx):
        db = pymysql.connect(host=DB_IP,user=DB_USER,password=DB_PASS,database=DB_DB, port=DB_PORT,charset='utf8')
        c = db.cursor()
        checkforchannel = "SELECT channelusinguser FROM dmsupport WHERE `channelusinguser` = '%s'"
        c.execute(checkforchannel, ctx.channel.id)

        checking = c.fetchone()

        try:
            strtoint = int(''.join(map(str, checking)))
        except:
            return await ctx.send("The channel you are trying to close is not a ticket!", delete_after=5.0)
        else:

            #Update the value that checks if that channel is a ticket right now and stop listening to specific user help.
            setticketuser = "UPDATE `dmsupport` SET `isuserticketing` = %s WHERE `channelusinguser` = '%s'"
            c.execute(setticketuser, (False, ctx.channel.id))

            #Get the ticket number            
            ticketnumberis = "SELECT rowid FROM dmsupport WHERE `channelusinguser` = '%s' ORDER BY rowid DESC LIMIT 1"
            c.execute(ticketnumberis, ctx.channel.id)
            check = c.fetchone()
            ticketNumber = int(''.join(map(str, check)))

            #Get the user that's receiving support
            getuserforannounce = "SELECT supportuser_id FROM dmsupport WHERE `channelusinguser` = '%s' ORDER BY rowid DESC LIMIT 1"
            c.execute(getuserforannounce, ctx.channel.id)
            brother = c.fetchone()
            userid = int(''.join(map(str, brother)))
            db.commit()

            realuser = self.bot.get_user(userid)
            
            closedtickets = discord.utils.get(ctx.guild.channels, id=720321456223027220)
            await ctx.channel.edit(name=f'closed {ticketNumber}', category=closedtickets)
            
            await realuser.send('Your ticket has been closed!')
            db.close()
            return await ctx.send("Channel closed succesfully!")

    @commands.command(hidden=True)
    @commands.has_role('Support')
    async def avail(self, ctx):
        db = pymysql.connect(host=DB_IP,user=DB_USER,password=DB_PASS,database=DB_DB, port=DB_PORT,charset='utf8')
        c = db.cursor()
        setsupport = "UPDATE `oplist` SET `support_available` = %s WHERE `operator_id` = '%s'"
        try:
            c.execute(setsupport, (True, ctx.author.id))
            db.commit()
            db.close()
            return await ctx.send('OK!')
        except:
            return await ctx.send('You are already receiving support requests!')
    
    @commands.command(hidden=True)
    @commands.has_role('Support')
    async def unavail(self, ctx):
        db = pymysql.connect(host=DB_IP,user=DB_USER,password=DB_PASS,database=DB_DB, port=DB_PORT,charset='utf8')
        c = db.cursor()
        setsupport = "UPDATE `oplist` SET `support_available` = %s WHERE `operator_id` = '%s'"
        try:
            c.execute(setsupport, (False, ctx.author.id))
            db.commit()
            db.close()
            return await ctx.send('OK!')
        except:
            return await ctx.send('You are **NOT** receiving support requests yet!')


    async def support_startup(self, message):
        guild = message.guild
        
        if not guild:
            db = pymysql.connect(host=DB_IP,user=DB_USER,password=DB_PASS,database=DB_DB, port=DB_PORT,charset='utf8')
            c = db.cursor()
            checkifuserticketing = "SELECT isuserticketing FROM dmsupport WHERE `supportuser_id` = '%s' ORDER BY rowid DESC LIMIT 1"
            c.execute(checkifuserticketing, message.author.id)
            check = c.fetchone()
            try:
                dbint = int(''.join(map(str, check)))
            except:
                dbint = 0
            
            if dbint == 1:
                
                lol = "SELECT channelusinguser FROM dmsupport WHERE `supportuser_id` = '%s' ORDER BY rowid DESC LIMIT 1"
                c.execute(lol, message.author.id)
                channelcheck = c.fetchone()
                channelid = int(''.join(map(str, channelcheck)))
                channel = self.bot.get_channel(channelid)
                embed = await createMSGEmbed(sender=message.author, message=message)
                return await channel.send(embed=embed)
            #if user in middle of a chat support session:
                #transcribe messages
                #support session finished? ->
                #return

            #FAQ Embed 1 For Entry
            if any([keyword in message.content.lower() for keyword in ('code', 'codes', 'redeem')]):
                embed = await createFAQEmbed(1)
                await StartSupport(self.bot, message, embed)

            #FAQ Entry 2
            elif any([keyword in message.content.lower() for keyword in ('save', 'saves')]):
                embed = await createFAQEmbed(2)
                await StartSupport(self.bot, message, embed)

            #FAQ Entry 3
            elif any([keyword in message.content.lower() for keyword in ('load', 'lowd', 'reload')]):
                embed = await createFAQEmbed(3)
                await StartSupport(self.bot, message, embed)

            #FAQ Entry 4
            elif any([keyword in message.content.lower() for keyword in ('levels', 'rank', 'ranks', 'role', 'roles', 'fat whale', 'whale')]):
                embed = await createFAQEmbed(4)
                await StartSupport(self.bot, message, embed)

            #FAQ Entry 5
            elif any([keyword in message.content.lower() for keyword in ('invite', 'discord', 'discord link')]):
                embed = await createFAQEmbed(5)
                await StartSupport(self.bot, message, embed)

            #FAQ Entry 6
            elif any([keyword in message.content.lower() for keyword in ('update', 'updates', 'updating')]):
                embed = await createFAQEmbed(6)
                await StartSupport(self.bot, message, embed)

            #FAQ Entry 7
            elif any([keyword in message.content.lower() for keyword in ('ping', 'pings', 'pinging')]):
                embed = await createFAQEmbed(7)
                await StartSupport(self.bot, message, embed)

            #FAQ Entry 8 
            elif any([keyword in message.content.lower() for keyword in ('refund', 'robux', 'gamepass')]):
                embed = await createFAQEmbed(8)
                await StartSupport(self.bot, message, embed)

            #FAQ Entry 9 
            elif any([keyword in message.content.lower() for keyword in ('bug', 'glitch', 'broke', 'report','error')]):
                embed = await createFAQEmbed(9)
                await StartSupport(self.bot, message, embed)

            #FAQ Entry 10
            elif any([keyword in message.content.lower() for keyword in ('suggest', 'idea', 'contribute')]):
                embed = await createFAQEmbed(10)
                await StartSupport(self.bot, message, embed)

            #FAQ Entry 11
            elif any([keyword in message.content.lower() for keyword in ('boat', 'marina', 'dock', 'harbor')]):
                embed = await createFAQEmbed(11)
                await StartSupport(self.bot, message, embed)


            #FAQ Entry 12
            elif any([keyword in message.content.lower() for keyword in ('rebirth', 'money')]):
                embed = await createFAQEmbed(12)
                await StartSupport(self.bot, message, embed)

            #FAQ Entry 13
            elif any([keyword in message.content.lower() for keyword in ('support', 'chat', 'help', 'assistance', 'ayuda')]):
                embed = await createFAQEmbed(13)
                await StartSupport(self.bot, message, embed)

            #FAQ Entry 14
            elif any([keyword in message.content.lower() for keyword in ('boost', 'nitro', 'perks')]):
                embed = await createFAQEmbed(14)
                await StartSupport(self.bot, message, embed)

            #FAQ Entry 15 
            elif any([keyword in message.content.lower() for keyword in ('instagram', 'twitter', 'social', 'youtube', 'discord')]):
                embed = await createFAQEmbed(15)
                await StartSupport(self.bot, message, embed)

            #FAQ Entry 16
            elif any([keyword in message.content.lower() for keyword in ('content', 'creator', 'stream')]):
                embed = await createFAQEmbed(16)
                await StartSupport(self.bot, message, embed)

            #FAQ Entry 17
            elif any([keyword in message.content.lower() for keyword in ('event', 'race', 'prize')]):
                embed = await createFAQEmbed(17)
                await StartSupport(self.bot, message, embed)

            else:
                nofaq = await message.author.send("Our Bot didn't find what you needed! \nDo you want so start a chat support session? - *Message Will be deleted in 60 seconds*")
                yes_emoji = '<:yes:724011319841390592>'
                no_emoji = '<:no:724011319887396915>'
                await nofaq.add_reaction(yes_emoji)
                await nofaq.add_reaction(no_emoji)
                def yes_no_check(reaction, user):
                    return user == message.author and str(reaction.emoji) in [yes_emoji, no_emoji]
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=yes_no_check)
                except asyncio.TimeoutError:
                    return
                else:
                    if str(reaction.emoji) == yes_emoji:
                        await message.author.send('<a:loading:724344921120833647> Starting Support Session now...')
                        ###from DMSupportChannel import support_time <---------------- This must be on the start of the file

                        ###return await support_time(message)
                        # ^^^^^^^^^ Will create and initiate the whole proccess of a DM Support Channel with the Bot(Staff Channel on Server)
                        #and the User requesting for help(DMs)
                        return await InmediateSupport(self.bot, message)
                    else:
                        await nofaq.delete()
                

            #print('The bot received a message in DMs!')
        else:
            if not message.channel.name.lower().startswith('ticket'):
                #print('Not a ticket!')
                return
            #print('It is a Ticket!')

            try:
            #Is the user a staff and the staff is sending messages in the ticket channel?
                db = pymysql.connect(host=DB_IP,user=DB_USER,password=DB_PASS,database=DB_DB, port=DB_PORT,charset='utf8')
                c = db.cursor()
                checkifuserticketing = "SELECT isuserticketing FROM dmsupport WHERE `staffuser_id` = '%s' ORDER BY rowid DESC LIMIT 1"
                c.execute(checkifuserticketing, message.author.id)
                check = c.fetchone()
                try:
                    dbint = int(''.join(map(str, check)))
                except:
                    dbint = 0

                if dbint == 1:
                    checkchannel = "SELECT channelusinguser FROM dmsupport WHERE `staffuser_id` = '%s' ORDER BY rowid DESC LIMIT 1"
                    c.execute(checkchannel, message.author.id)
                    check = c.fetchone()
                    channelsrvid = int(''.join(map(str, check)))

                    if channelsrvid == message.channel.id:
                        getdm = "SELECT supportuser_id FROM dmsupport WHERE `staffuser_id` = '%s' ORDER BY rowid DESC LIMIT 1"
                        c.execute(getdm, message.author.id)
                        checkstaff = c.fetchone()
                        userinDMs = int(''.join(map(str, checkstaff)))
                        #Message sent in the ticket channel
                        supportuser = self.bot.get_user(userinDMs)
                        closetuple = ('-close', '-!close', '--n')
                        if message.content.lower().startswith(closetuple):
                            return
                        elif message.content.lower().endswith('--n'):
                            return

                        embed = await createMSGEmbed(sender=message.author, message=message)
                        return await supportuser.send(embed=embed)
            except:
            #     #He's not. return
                return

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        await self.support_startup(message)
        




if __name__ != "__main__":
        print('Support Time is Ready!')

def setup(bot):
    bot.add_cog(DMSupport(bot))