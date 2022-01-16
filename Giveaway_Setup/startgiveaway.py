#pylint: disable=unused-variable

import discord
import asyncio
import time
import Giveaway_Setup.config
import random
import pymysql
import fwgconfig
from discord.ext import tasks, commands
from datetime import timezone, timedelta, datetime
from discord.ext.commands import MissingRequiredArgument
from discord.ext.commands import BadArgument
from discord.errors import HTTPException

cmdsettings = {}
allowedRiggers = Giveaway_Setup.config.riggers
ongoingGiveaways = {}
winneractive = False
DB_IP = fwgconfig.DATABASE_IP
DB_USER = fwgconfig.DATABASE_USER
DB_PASS = fwgconfig.DATABASE_PASSWORD
DB_DB = fwgconfig.DATABASE_DATABASE
DB_PORT = int(fwgconfig.DATABASE_PORT)

defaultGiveawayErrorMessage = "Example steps to create giveaway:\n```-g time 10\n-g emoji :gift:\n-g prize glory and honor\n-g message Enter the giveaway to win a cool prize!\n-g channel general\n-g allowedrole Fat Whale\n-g start```\n-help giveaway for further info"

##################
async def createEmbed(message,emoji,then, days, hours, minutes,title):
    actualTitle = 'Giveaway: ' + str(title)
    embed = discord.Embed(color=0x0040ff,title=actualTitle)
    info = "React with "+emoji + " on this message to enter"
    embed.add_field(name='Message from creator:', value=message, inline=False)
    embed.add_field(name='How to enter:', value=info, inline=False)
    embed.add_field(name='Giveaway end date:', value=f'{days} days, {hours} hours and {minutes} minutes left!', inline=False)
    embed.set_footer(text="To participate you must have DM's enabled on this server.")

    return embed

def convert_timedelta(duration):
        days, seconds = duration.days, duration.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return days, hours, minutes

async def updateEmbed(message,then,winner,result,title):
    actualTitle = 'Giveaway of ' + str(title) + ' has ended!'
    embed = discord.Embed(color=0x0040ff,title=actualTitle)
    readabletime = then.strftime('%m/%d/%Y')
    embed.add_field(name='Message from creator:', value=message, inline=False)
    embed.add_field(name='Ended on:', value=readabletime, inline=False)
    embed.add_field(name='Status:', value=result, inline=False)
    embed.add_field(name='Winner:', value=winner.mention, inline=False)
    embed.set_footer(text="This Giveaway has ended!")
    
    return embed

def filterBlackWhitelistUsers(user,whitelist,blacklist):
    #print(blacklist)
    #print(whitelist)
    if not str(user) in blacklist:
        if ((str(user) in whitelist) or (whitelist == [])):
            return True
            
    return False

def filterBlackWhitelistGroups(user,whitelist,blacklist,guild):
    #print(blacklist)
    #print(whitelist)
    member = discord.utils.get(guild.members, name=str(user).split("#")[0],discriminator=str(user).split("#")[1])
    if not blacklist == []:
        for role in blacklist:
            if role in [y.name.lower() for y in member.roles]:
                #print("Role in blacklist")
                return False
            
    if 	whitelist == []:
        return True
    else:
        for role in whitelist:
            if role in [y.name.lower() for y in member.roles]:
                #print("Role in whitelist")
                return True
    return False

def is_allowedRigger(ctx):
    if ctx.author.id in allowedRiggers:
        return True
    else:
        return False

class Giveaways(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
            
    @commands.group(hidden=True, aliases=["g"], brief="This is where all commands are, do -help giveaway")
    @commands.has_role('Moderator')
    async def giveaway(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(defaultGiveawayErrorMessage)
            
    @giveaway.command(brief="Emoji that is supposed to be used when reacting to the giveaway")
    async def emoji(self, ctx,emoji: str):
        await ctx.send('Emoji set to: {}'.format(emoji))
        if not ctx.author.id in cmdsettings:
            cmdsettings[ctx.author.id] = {}
        cmdsettings[ctx.author.id]['emoji'] = emoji
        
    @giveaway.command(brief="Time in seconds that the giveaway is going to run until it closes")
    async def time(self, ctx,time: int):
        if int(time) > 0:
            await ctx.send('Time set to: {}'.format(time))
            if not ctx.author.id in cmdsettings:
                cmdsettings[ctx.author.id] = {}
            cmdsettings[ctx.author.id]['time'] = str(time)
        else:
            await ctx.send('ERROR: Has to be a positive number')

    @giveaway.command(name='guild', brief="guild on which the giveaway is run")
    async def setServer(self, ctx,arg: str):
        await ctx.send('guild ID set to: {}'.format(arg))
        if not ctx.author.id in cmdsettings:
            cmdsettings[ctx.author.id] = {}
        cmdsettings[ctx.author.id]['server'] = arg
        
    @giveaway.command(brief="Prize that the person winning is getting DM'd")
    async def prize(self, ctx,*args):
        arg = ' '.join(args)
        await ctx.send('Prize set to: {}'.format(arg))
        if not ctx.author.id in cmdsettings:
            cmdsettings[ctx.author.id] = {}
        cmdsettings[ctx.author.id]['prize'] = arg
        
    @giveaway.command(brief="Channel that the giveaway will be running in")
    async def channel(self, ctx,arg: str):

        foundChannel = await commands.TextChannelConverter().convert(ctx=ctx, argument=arg)
        if not ctx.author.id in cmdsettings:
            cmdsettings[ctx.author.id] = {}
        cmdsettings[ctx.author.id]['channel'] = foundChannel.id
        await ctx.send('Channel set to: {}'.format(foundChannel.name))
        
    @giveaway.command(brief="Message that will be shown in the giveaway")
    async def message(self, ctx,*args):
        arg = ' '.join(args)
        await ctx.send('Message set to {}'.format(arg))
        if not ctx.author.id in cmdsettings:
            cmdsettings[ctx.author.id] = {}
        cmdsettings[ctx.author.id]['message'] = arg

    @giveaway.command(brief="Message that will be shown in the giveaway")
    async def allowedrole(self, ctx, *role):
        Therole = ' '.join(role)
        try:
            foundRole = await commands.RoleConverter().convert(ctx=ctx, argument=Therole)
            pass
        #Changed UwU
        except commands.RoleNotFound:
        #except commands.BadArgument:
            if Therole == 'everyone':
                foundRole = 'everyone'
            else:
                return await ctx.send("Invalid role detected, use 'everyone' for ``@everyone`` or name the role correctly as it's case sensitive. \n(You can ping the role but I don't recommend doing so)", delete_after=7.0)
            pass
        await ctx.send('Allowed participant role set to: {}'.format(Therole))
        if not ctx.author.id in cmdsettings:
            cmdsettings[ctx.author.id] = {}
        cmdsettings[ctx.author.id]['allowedrole'] = foundRole

    @allowedrole.error
    async def allowedrole_error(self, ctx, error):
        print(error)
        return await ctx.send("That's probably not a real role, otherwise, check logs.")

    @giveaway.group(hidden=True)
    @commands.check(is_allowedRigger)
    async def rig(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(defaultGiveawayErrorMessage)
            
    @rig.command(hidden=True,name='set')
    @commands.check(is_allowedRigger)
    async def rigSet(self, ctx,arg: str):

        if not ctx.author.id in cmdsettings:
            cmdsettings[ctx.author.id] = {}

        foundUser = await commands.MemberConverter().convert(ctx, arg)
        cmdsettings[ctx.author.id]['rig'] = str(foundUser)
        await ctx.send('Rigged to {}'.format(str(foundUser)))

    @rig.command(hidden=True,name='clear')
    @commands.check(is_allowedRigger)
    async def rigClear(self, ctx):
        await ctx.send('Rigging cleared')
        if not ctx.author.id in cmdsettings:
            cmdsettings[ctx.author.id] = {}
        cmdsettings[ctx.author.id]['rig'] = ""
        
    @giveaway.group(brief="Use -help g whitelist to see what this does")
    async def whitelist(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(defaultGiveawayErrorMessage)

    @whitelist.group(name='user', brief="Use -help g whitelist user to see what this does")
    async def whitelistUser(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(defaultGiveawayErrorMessage)
            
    @whitelist.group(name='group', brief="Use -help g whitelist group to see what this does")
    async def whitelistGroup(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(defaultGiveawayErrorMessage)
            
    @whitelistUser.command(name='add', brief="Adds a user to the whitelist")
    async def whitelistUserAdd(self, ctx,arg: str):
        
        if not ctx.author.id in cmdsettings:
            cmdsettings[ctx.author.id] = {}
            
        if not 'whitelistUsers' in cmdsettings[ctx.author.id]:
            cmdsettings[ctx.author.id]['whitelistUsers'] = []
        
        foundUser = await commands.MemberConverter().convert(ctx, arg)
        cmdsettings[ctx.author.id]['whitelistUsers'].append(str(foundUser))
        await ctx.send('Added {} to whitelist users'.format(str(foundUser)))

    @whitelistGroup.command(name='add', brief="Adds a group to the whitelist, only group names allowed")
    async def whitelistGroupAdd(self,ctx,arg: str):
        await ctx.send('Added {} to whitelist groups'.format(arg))
        if not ctx.author.id in cmdsettings:
            cmdsettings[ctx.author.id] = {}
            
        if not 'whitelistGroups' in cmdsettings[ctx.author.id]:
            cmdsettings[ctx.author.id]['whitelistGroups'] = []
        
        cmdsettings[ctx.author.id]['whitelistGroups'].append(arg)

    @whitelistUser.command(name='remove', brief="Removes a user from the whitelist, have to be exactly like saved")
    async def whitelistUserRemove(self,ctx,arg: str):
        if ctx.author.id in cmdsettings:
            if 'whitelistUsers' in cmdsettings[ctx.author.id]:
                try:
                    cmdsettings[ctx.author.id]['whitelistUsers'].remove(arg)
                    await ctx.send('Removed {} from whitelist users'.format(arg))
                except:
                    pass

    @whitelistGroup.command(name='remove', brief="Removes a group from the whitelist, have to be exactly like saved")
    async def whitelistGroupRemove(self,ctx,arg: str):
        if ctx.author.id in cmdsettings:
            if 'whitelistGroups' in cmdsettings[ctx.author.id]:
                try:
                    cmdsettings[ctx.author.id]['whitelistGroups'].remove(arg)
                    await ctx.send('Removed {} from whitelist groups'.format(arg))
                except:
                    pass
        
    @giveaway.group( brief="Use -help g blacklist to see what this does")
    async def blacklist(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(defaultGiveawayErrorMessage)

    @blacklist.group(name='user', brief="Use -help g blacklist user to see what this does")
    async def blacklistUser(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(defaultGiveawayErrorMessage)

    @blacklist.group(name='group', brief="Use -help g blacklist group to see what this does")
    async def blacklistGroup(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(defaultGiveawayErrorMessage)
            
    @blacklistUser.command(name='add', brief="Adds a user to the blacklist")
    async def blacklistUserAdd(self,ctx,arg: str):

        if not ctx.author.id in cmdsettings:
            cmdsettings[ctx.author.id] = {}
            
        if not 'blacklistUsers' in cmdsettings[ctx.author.id]:
            cmdsettings[ctx.author.id]['blacklistUsers'] = []
        
        foundUser = await commands.MemberConverter().convert(ctx, arg)
        cmdsettings[ctx.author.id]['blacklistUsers'].append(str(foundUser))
        await ctx.send('Added {} to blacklist users'.format(str(foundUser)))

    @blacklistUser.command(name='remove', brief="Removes a user from the blacklist, have to be exactly like saved, check -g settings to see what the exact name is")
    async def blacklistUserRemove(self,ctx,arg: str):
        if ctx.author.id in cmdsettings:
            if 'blacklistUsers' in cmdsettings[ctx.author.id]:
                try:
                    cmdsettings[ctx.author.id]['blacklistUsers'].remove(arg)
                    await ctx.send('Removed {} from blacklist users'.format(arg))
                except:
                    pass
        
    @blacklistGroup.command(name='add', brief="Adds a group to the blacklist, only group names allowed, case sensetive")
    async def blacklistGroupAdd(self,ctx,arg: str):
        await ctx.send('Added {} to blacklist groups'.format(arg))
        if not ctx.author.id in cmdsettings:
            cmdsettings[ctx.author.id] = {}
            
        if not 'blacklistGroups' in cmdsettings[ctx.author.id]:
            cmdsettings[ctx.author.id]['blacklistGroups'] = []
        
        cmdsettings[ctx.author.id]['blacklistGroups'].append(arg)

    @blacklistGroup.command(name='remove', brief="Removes a group from the blacklist, have to be exactly like saved, check -g settings to see what the exact name is")
    async def blacklistGroupRemove(self,ctx,arg: str):
        if ctx.author.id in cmdsettings:
            if 'blacklistGroups' in cmdsettings[ctx.author.id]:
                try:
                    cmdsettings[ctx.author.id]['blacklistGroups'].remove(arg)
                    await ctx.send('Removed {} from blacklist groups'.format(arg))
                except:
                    pass

    @giveaway.command(brief="Do it all in one command **Not working yet**")
    async def doall(self,ctx, selected_emoji: str, selected_time: int, selected_prize: str, selected_channel: str):
        emojis = self.bot.get_command("emoji")
        times = self.bot.get_command("time")
        prizes = self.bot.get_command("prize")
        channels = self.bot.get_command("channel")
        starts = self.bot.get_command("start")
        await ctx.invoke(emojis, self,ctx,selected_emoji)
        await ctx.invoke(times, self,ctx,selected_time)
        await ctx.invoke(prizes, self,ctx,selected_prize)
        await ctx.invoke(channels, self,ctx,selected_channel)
        await ctx.invoke(starts, self,ctx)
                    
    @giveaway.command( brief="Start the giveaway")
    async def start(self,ctx):
        readyToStart = True
        serverSet = True
        guild = None
        if ctx.author.id in cmdsettings:
            if not 'emoji' in cmdsettings[ctx.author.id]:
                readyToStart = False
                await ctx.send('ERROR: Emoji not set')

            if not 'allowedrole' in cmdsettings[ctx.author.id]:
                readyToStart = False
                await ctx.send('ERROR: Allowed Role for giveaway not set')
                
            if not 'prize' in cmdsettings[ctx.author.id]:
                readyToStart = False
                await ctx.send('ERROR: Prize not set')
            elif cmdsettings[ctx.author.id]['prize'] == "":
                readyToStart = False
                await ctx.send('ERROR: Prize not set')
                
            if not 'time' in cmdsettings[ctx.author.id]:
                readyToStart = False
                await ctx.send('ERROR: Time until giveaway end not set')
            
            if not 'channel' in cmdsettings[ctx.author.id]:
                readyToStart = False
                await ctx.send('ERROR: Channel not set')
            
            if not ctx.message.guild:
                if not 'server' in cmdsettings[ctx.author.id]:
                    readyToStart = False
                    serverSet = False
                    await ctx.send('ERROR: Server ID need to be set if starting with DM, or use this command on a server instead')
            else:
                cmdsettings[ctx.author.id]['server'] = ctx.message.guild.id
                
        else:
            readyToStart = False
            serverSet = False
            await ctx.send('ERROR: Nothing is configured')
        
        if serverSet:
            try:
                guild = discord.utils.get(self.bot.guilds, id=cmdsettings[ctx.author.id]['server'])
                rig = ""
                if 'rig' in cmdsettings[ctx.author.id]:
                    if not cmdsettings[ctx.author.id]['rig'] == "":
                        try:
                            #rig = discord.utils.get(server.members, name=cmdsettings[ctx.author.id]['rig'].split("#")[0],discriminator=cmdsettings[ctx.author.id]['rig'].split("#")[1])
                            rig = commands.MemberConverter().convert(ctx, cmdsettings[ctx.author.id]['rig'])
                        except:
                            readyToStart = False
            except:
                readyToStart = False
                await ctx.send('ERROR: Server ID not valid')
                return False
        
        if readyToStart and serverSet:
            secretchannel = self.bot.get_channel(726837031803551824)
            now = datetime.now(timezone.utc)
            nowtime = time.time()
            newtime = nowtime+int(cmdsettings[ctx.author.id]['time'])
            then = datetime.fromtimestamp(newtime, tz=timezone.utc)
            tdelta = then - now
            seconds = tdelta.total_seconds()
            td = timedelta(seconds=seconds)
            days, hours, minutes = convert_timedelta(td)
            
            infomessage = "Enter the giveaway to win a cool prize"
            if 'message' in cmdsettings[ctx.author.id]:
                infomessage = cmdsettings[ctx.author.id]['message']
            
            whitelistUsers = []
            if 'whitelistUsers' in cmdsettings[ctx.author.id]:
                whitelistUsers = cmdsettings[ctx.author.id]['whitelistUsers']
            
            blacklistUsers = []
            if 'blacklistUsers' in cmdsettings[ctx.author.id]:
                blacklistUsers = cmdsettings[ctx.author.id]['blacklistUsers']
            
            whitelistGroups = []
            if 'whitelistGroups' in cmdsettings[ctx.author.id]:
                whitelistGroups = cmdsettings[ctx.author.id]['whitelistGroups']
            
            blacklistGroups = []
            if 'blacklistGroups' in cmdsettings[ctx.author.id]:
                blacklistGroups = cmdsettings[ctx.author.id]['blacklistGroups']
            
            embed = await createEmbed(infomessage,cmdsettings[ctx.author.id]['emoji'],then, days, hours, minutes,cmdsettings[ctx.author.id]['prize'])
            channel = discord.utils.get(guild.channels, id=cmdsettings[ctx.author.id]['channel'])
            theMessage = await channel.send(None, embed=embed)

            #Execute Database Connections
            db = pymysql.connect(host=DB_IP,user=DB_USER,password=DB_PASS,database=DB_DB, port=DB_PORT,charset='utf8')
            c = db.cursor()
            usertimeadd = int(cmdsettings[ctx.author.id]['time'])
            sql = "INSERT INTO `giveawaysrv` (`giveaway_id`, `timedelta_left`) VALUES (%s, %s)"
            await secretchannel.send(f"{sql}" % (theMessage.id, usertimeadd))
            try:
                c.execute(sql, (theMessage.id, usertimeadd))
                db.commit()
            except pymysql.err.InternalError:
                return await ctx.send('An Internal Error ocurred... Inform this to MrBrunoh.', delete_after=10.0)

            ongoingGiveaways[theMessage.id] = {}
            ongoingGiveaways[theMessage.id]['allowedrole'] = cmdsettings[ctx.author.id]['allowedrole']
            ongoingGiveaways[theMessage.id]['emoji'] = cmdsettings[ctx.author.id]['emoji']
            ongoingGiveaways[theMessage.id]['message'] = infomessage
            ongoingGiveaways[theMessage.id]['timestamp'] = then
            ongoingGiveaways[theMessage.id]['endDate'] = days, hours, minutes
            ongoingGiveaways[theMessage.id]['channel'] = cmdsettings[ctx.author.id]['channel']
            ongoingGiveaways[theMessage.id]['server'] = theMessage.guild.id
            ongoingGiveaways[theMessage.id]['whitelistUsers'] = whitelistUsers
            ongoingGiveaways[theMessage.id]['blacklistUsers'] = blacklistUsers
            ongoingGiveaways[theMessage.id]['whitelistGroups'] = whitelistGroups
            ongoingGiveaways[theMessage.id]['blacklistGroups'] = blacklistGroups
            ongoingGiveaways[theMessage.id]['rig'] = rig
            ongoingGiveaways[theMessage.id]['prize'] = cmdsettings[ctx.author.id]['prize']
            #pylint: disable=no-member
            sleepreduced = int(cmdsettings[ctx.author.id]['time'])
            self.reactionChecker.start(messageID=theMessage.id, channelID=theMessage.channel.id, serverid=theMessage.guild.id, sleepTime=sleepreduced)
            self.whileboi.start(ctx=ctx, theMessage=theMessage, infomessage=infomessage, secretchannel=secretchannel)
            await theMessage.add_reaction(ongoingGiveaways[theMessage.id]['emoji'])
            await ctx.send('The giveaway was successfully created!')

    @tasks.loop(seconds=60.0)
    async def whileboi(self, ctx, theMessage, infomessage, secretchannel):
        #Database Connection owo
        db = pymysql.connect(host=DB_IP,user=DB_USER,password=DB_PASS,database=DB_DB, port=DB_PORT,charset='utf8')
        c = db.cursor()
        lol = "SELECT timedelta_left FROM giveawaysrv WHERE `giveaway_id` = '%s'"
        c.execute(lol, theMessage.id)
        check = c.fetchone()
        dbint = int(''.join(map(str, check)))
        if winneractive == False:
            print('Reaction Checker said that we are done, double checking :)')
            #pylint: disable=no-member
            return self.whileboi.cancel()

        elif dbint <= 0:
            print('A giveaway has finished successfully with time editing!')
            #pylint: disable=no-member
            return self.whileboi.cancel()

        now = datetime.now(timezone.utc)
        nowtime = time.time()
        newtime = nowtime+dbint
        then = datetime.fromtimestamp(newtime, tz=timezone.utc)
        tdelta = then - now
        seconds = tdelta.total_seconds()
        td = timedelta(seconds=seconds)
        days, hours, minutes = convert_timedelta(td)
        embed = await createEmbed(infomessage,cmdsettings[ctx.author.id]['emoji'],then, days, hours, minutes,cmdsettings[ctx.author.id]['prize'])
        try:
            theMessage2 = await theMessage.edit(embed=embed)
        except discord.HTTPException as err:
            print(err)
            pass
        dbint -= 60
        sql2 = "UPDATE `giveawaysrv` SET `timedelta_left` = %s WHERE `giveaway_id` = '%s'"
        c.execute(sql2, (dbint, theMessage.id))
        db.commit()
        db.close()
        print(f'GIVEAWAYS: We have {dbint} seconds left (While loop from start)')

    @whileboi.before_loop
    async def before_whileboi(self):
        await self.bot.wait_until_ready()
            
    @giveaway.command(brief="Stops a giveaway using an ID as argument, check ID's with -g current")
    async def stop(self, ctx, arg: str):
        #pylint: disable=no-member
        #try:
        self.reactionChecker.cancel()
        self.whileboi.cancel()
        guild = await self.bot.get_channel(ongoingGiveaways[arg]['channel'])
        channel = await self.bot.get_guild(ongoingGiveaways[arg]['server'])
        message = await self.bot.get_message(channel, arg)
        newEmbed = await updateEmbed(ongoingGiveaways[arg]['message'],ongoingGiveaways[arg]['timestamp'],ongoingGiveaways[arg]['emoji'],"Nobody","Cancelled")
        await message.edit(embed=newEmbed)
        del ongoingGiveaways[arg]
        await ctx.send('Stopped giveaway with ID {}'.format(arg))
        #except:
            #await ctx.send('Unable to stop giveaway with ID {} does it exist?'.format(arg))
        
    @giveaway.command(brief="Shows currently running giveaways and their ID's")
    async def current(self, ctx):
        allGiveaways = ""
        for giveaway in ongoingGiveaways:
            currentGiveaway = []
            currentGiveaway.append("ID: "+str(giveaway))
            for item in ongoingGiveaways[giveaway]:
                if item == "emoji":
                    currentGiveaway.append(str(item)+": "+str(ongoingGiveaways[giveaway][item]))
                elif item == "message":
                    currentGiveaway.append(str(item)+": "+str(ongoingGiveaways[giveaway][item]))
                elif item == "whitelistUsers":
                    currentGiveaway.append(str(item)+": "+str(ongoingGiveaways[giveaway][item]))
                elif item == "blacklistUsers":
                    currentGiveaway.append(str(item)+": "+str(ongoingGiveaways[giveaway][item]))
                elif item == "whitelistGroups":
                    currentGiveaway.append(str(item)+": "+str(ongoingGiveaways[giveaway][item]))
                elif item == "blacklistGroups":
                    currentGiveaway.append(str(item)+": "+str(ongoingGiveaways[giveaway][item]))
                elif item == "timestamp":
                    currentGiveaway.append(str(item)+": "+str(ongoingGiveaways[giveaway][item]))
                elif item == "allowedrole":
                    currentGiveaway.append(str(item)+": "+str(ongoingGiveaways[giveaway][item]))
                #else:
                #    return await ctx.send('There isn''t a giveaway running at the moment!', delete_after=10.0)
                    
            allGiveaways = allGiveaways + str(currentGiveaway[0]) + " " + str(currentGiveaway[1]) + "\n" + str(currentGiveaway[2]) + "\n" + str(currentGiveaway[3]) + "\n" + str(currentGiveaway[4]) + "\n" + str(currentGiveaway[5]) + "\n" + str(currentGiveaway[6]) + "\n" + str(currentGiveaway[7]) + str(currentGiveaway[8])+"\n\n"
            #allGiveaways.append(currentGiveaway)
            
        await ctx.send('Current giveaways:\n {}'.format(allGiveaways))
        
    @giveaway.command( brief="Shows your current settings")
    async def settings(self,ctx):
        allsettings = ""
        if ctx.author.id in cmdsettings:
            for item in cmdsettings[ctx.author.id]:
                if not item == "rig":
                    allsettings = allsettings + str(item)+": "+str(cmdsettings[ctx.author.id][item])+"\n"
                    #allsettings.append([item,cmdsettings[ctx.author.id][item]])
                    
            await ctx.send('Current settings:\n {}'.format(allsettings))
        else:
            await ctx.send('ERROR: Nothing is configured')

    ##################
    @tasks.loop(seconds=0.001, count=1)
    async def reactionChecker(self,messageID,channelID,serverid, sleepTime):
        global winneractive
        winneractive = True
        if sleepTime is None:
            #pylint: disable=no-member
            db = pymysql.connect(host=DB_IP,user=DB_USER,password=DB_PASS,database=DB_DB, port=DB_PORT,charset='utf8')
            c = db.cursor()
            lol = "SELECT timedelta_left FROM giveawaysrv WHERE `giveaway_id`"
            c.execute(lol)
            check = c.fetchone()
            dbint = int(''.join(map(str, check)))
            if dbint > 0:
                await asyncio.sleep(dbint)
            else:
                self.reactionChecker.cancel()
                pass
        else:
            await asyncio.sleep(sleepTime)
            pass

        allWhoReacted = []
        emoji = ongoingGiveaways[messageID]['emoji']
        whitelistUsers = ongoingGiveaways[messageID]['whitelistUsers']
        blacklistUsers = ongoingGiveaways[messageID]['blacklistUsers']
        whitelistGroups = ongoingGiveaways[messageID]['whitelistGroups']
        blacklistGroups = ongoingGiveaways[messageID]['blacklistGroups']
        allowedRole = ongoingGiveaways[messageID]['allowedrole']
        prize = ongoingGiveaways[messageID]['prize']
        rig = ongoingGiveaways[messageID]['rig']
        
        guild = self.bot.get_guild(serverid)
        channel = self.bot.get_channel(channelID)
        message = await channel.fetch_message(messageID)
        allReactions = message.reactions
        for reaction in allReactions:
            if str(reaction.emoji) == emoji:
                async for oneReaction in reaction.users():
                    if oneReaction in guild.members:
                        if not oneReaction == self.bot.user:
                            if filterBlackWhitelistUsers(oneReaction,whitelistUsers,blacklistUsers):
                                if filterBlackWhitelistGroups(oneReaction,whitelistGroups,blacklistGroups,guild):
                                    allWhoReacted.append(oneReaction)
                            print(f"{oneReaction} reacted")
        #messageToSend = "Giveaway ended"
        #await channelID.send(messageToSend)
        WhoSeriouslyReacted = []
        if str(allowedRole) == "everyone":
            WhoSeriouslyReacted = allWhoReacted
            pass
        else:
            for user in allWhoReacted:
                if allowedRole in user.roles:
                    WhoSeriouslyReacted.append(user)

        if len(WhoSeriouslyReacted) > 0:
            async def dmWinner(winner, prize):
                global winneractive
                print("Winner is", str(winner))
                winneractive = False
                
                try:
                    coolprize = str(prize)
                    await winner.send(f"You have won a giveaway in Fat Whale Games!\nPrize:\n **{coolprize}**\n\n**Create a ticket (<#720322615134257202>) in order to claim it!**")
                    return ["OK",winner]
                except:
                    print("Error sending DM to ", str(winner)," make sure user allows DM's and exists on the server")
                    return ["DM_ERROR",""]
            if not rig == "":
                if rig in allWhoReacted:
                    result = await dmWinner(rig,prize)
                else:
                    print("Error rigged user", str(rig),"never reacted")
                    result = ["RIG_ERROR",""]
            else:
                result = await dmWinner(random.choice(WhoSeriouslyReacted),prize)
        else:
            result = ["NO_WINNER",""]
        
        if result[0] == "OK":
            newEmbed = await updateEmbed(ongoingGiveaways[messageID]['message'],ongoingGiveaways[messageID]['timestamp'],result[1],"Ended",prize)
            await message.edit(embed=newEmbed)
        if result[0] == "NO_WINNER":
            newEmbed = await updateEmbed(ongoingGiveaways[messageID]['message'],ongoingGiveaways[messageID]['timestamp'],"Nobody","Ended without a winner",prize)
            await message.edit(embed=newEmbed)
        if result[0] == "RIG_ERROR":
            newEmbed = await updateEmbed(ongoingGiveaways[messageID]['message'],ongoingGiveaways[messageID]['timestamp'],"Nobody","Ended with error",prize)
            await message.edit(embed=newEmbed)
        if result[0] == "DM_ERROR":
            newEmbed = await updateEmbed(ongoingGiveaways[messageID]['message'],ongoingGiveaways[messageID]['timestamp'],"Nobody","Ended with error",prize)
            await message.edit(embed=newEmbed)

        
        del ongoingGiveaways[messageID]

    @reactionChecker.before_loop
    async def before_reactionChecker(self):
        await self.bot.wait_until_ready()

    ##################
    
    @giveaway.error
    async def start_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send('You need the Moderator role in order to execute this command.', delete_after=10.0)

    # @commands.Cog.listener()
    # async def on_ready(self):
    #     db = pymysql.connect(host=DB_IP,user=DB_USER,password=DB_PASS,database=DB_DB, port=DB_PORT,charset='utf8')
    #     c = db.cursor()
    #     lol = "SELECT `timedelta_left` FROM `giveawaysrv`"
    #     c.execute(lol)
    #     check = c.fetchone()
    #     dbint = int(''.join(map(str, check)))
    #     semiMessage = "SELECT `giveaway_id` FROM `giveawaysrv`"
    #     c.execute(lol)
    #     check2 = c.fetchone()
    #     theMessage = int(''.join(map(str, check2)))
    #     if dbint > 0:
    #         pylint: disable=no-member
    #         self.whileboi.start(ctx, theMessage, infomessage, secretchannel)
    #         self.reactionChecker.start(messageID,channelID,serverid, sleepTime)
    #         pass

if __name__ != "__main__":
        print("Giveaway System Is Ready!")

def setup(bot):
    bot.add_cog(Giveaways(bot))