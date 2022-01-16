#pylint: disable=unused-variable
#pylint: disable=unused-argument
#pylint: disable=W1401
#pylint: disable=F0401

import discord
import asyncio
import emoji
import traceback
import os
#Database Entries and More
import fwgconfig
#Some operator things
from Databases import sparked_db
from Extension_Commands import reportbug
from discord.ext import commands
from discord.ext.commands import CommandNotFound, MissingRequiredArgument, BadArgument, CommandOnCooldown

#BOTTOM WILL DEBUG EVERY ASYNC TASK THAT HAPPENS (YES YES SIR)
#os.environ["PYTHONASYNCIODEBUG"] = "1"


description = '''The Private Multi-task Fat Whales Games Bot\n Made by MrBrunoh. (Version 3.0 Stable - Now this bot works only on Airplane Simulator)'''
bot = commands.Bot(command_prefix='-', description=description, case_insensitive=True, intents=discord.Intents.all(), debug_guilds=[856678143608094751])
bot.remove_command("help")

#List of users with operative powers in the server. (Generally Moderators and above)


verifyint = 0
DB_IP = fwgconfig.DATABASE_IP
DB_USER = fwgconfig.DATABASE_USER
DB_PASS = fwgconfig.DATABASE_PASSWORD
DB_DB = fwgconfig.DATABASE_DATABASE
DB_PORT = int(fwgconfig.DATABASE_PORT)

#Disable normal help command

#bot.remove_command("help")

#Read the token in a private.txt file.
readtoken = open("token.txt","r")
if readtoken.mode == "r":
    contents = readtoken.read()
else:
    print('Error During the TOKEN reading, please check the file or the code.')
mythicaltoken = str(contents)

extensions = [
              "Important.messages",
              "Databases.sparked_db",
              ###"Moderation.mod_commands",
              "Fun_Commands.misc_commands",
              "Fun_Commands.TTT",
              "Fun_Commands.minesweeper",
              #Load extension_commands because i'd like to separate each one of those lol
              "Extension_Commands.reportbug",
              "Extension_Commands.suggest",
              "Extension_Commands.suggestplanes",
              "Extension_Commands.Administrative.admincmds",
              ###"Extension_Commands.boosters",
              "Extension_Commands.help",
              #"Giveaway_Setup.startgiveaway",
              #Music Startup - DISABLED BECAUSE OK
              #"Music_Service.musicmain",

              #DM Support Service
              #"DMSupport.dm_support_main"
              
              ]

for extension in extensions:
        try:
            bot.load_extension(extension)
            print(f'Loaded {extension} correctly!')
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print(f'Failed to load extension {extension}\n{exc}')

@bot.command(hidden=True)
@commands.has_role('Admin')
async def reloadcog(ctx, *, cog:str):
    try:
        bot.unload_extension(cog)
        bot.load_extension(cog)
        print(f'{cog} reloaded successfully!')
    except Exception as e:
        await ctx.send('{}: {}'.format(type(e).__name__, e))
    else:
        await ctx.send(f'Cog {cog} reloaded successfully!')

@bot.command(hidden=True)
@commands.has_role('Admin')
async def loadcog(ctx, *, cog:str):
    try:
        bot.load_extension(cog)
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        await ctx.send(f'Failed to load extension {extension}\n{exc}')
    else:
        await ctx.send(f'Cog {cog} lock n'' loaded successfully!')


@bot.event
async def on_ready():
    #Wait until the bot has loaded into discord
    await bot.wait_until_ready()
    #verifypurge.start()


    print(" /\------------------------------- Bot is ready and running! -------------------------------/\ ")

@bot.event
async def on_command_error(ctx, error):
    themessage = ctx.message
    if isinstance(error, CommandNotFound): return
    elif isinstance(error, MissingRequiredArgument):
        argerror = await ctx.send('Your command needs a required argument! Please check for misstypes, read the pins and try again.')
        await themessage.delete()
        await asyncio.sleep(7)
        await argerror.delete()
        return
    elif isinstance(error, BadArgument):
        argerror = await ctx.send('Your command includes an invalid argument! Maybe you typed an int where a boolean goes, or something else?')
        await themessage.delete()
        await asyncio.sleep(7)
        await argerror.delete()
        return
    elif isinstance(error, CommandOnCooldown):
        return await ctx.send('This command is on cooldown! Wait around ``10 seconds`` before executing it again.', delete_after=10.0)

    etype = type(error)
    trace = error.__traceback__
    lines = traceback.format_exception(etype, error, trace, limit=2)
    traceback_text = ''.join(lines)
    channel = bot.get_channel(920403679738204170)
    embed=discord.Embed(title=emoji.emojize("On_Command_Error Detected :tools:"), description=" ", color=0xFF0000)
    embed.set_author(name=bot.user, icon_url=bot.user.avatar.url)
    embed.set_thumbnail(url="https://www.freeiconspng.com/uploads/error-icon-15.png")
    embed.add_field(name="There was an error:", value=(traceback_text), inline=False)
    print("Error Logged:")
    print(traceback_text)
    try:
        await channel.send(embed=embed)
    except Exception:
        with open("traceback.txt", "x") as f:
            f.write(traceback_text)
        await channel.send(emoji.emojize('*On_Command_Error* Detected, Sending traceback file due to Discord Embed Limitations... :tools:'))
        await channel.send(file=discord.File('traceback.txt'))
        await asyncio.sleep(1)
        os.remove("traceback.txt")
    
async def shutdown():
    print("Closing connection to Discord...")
    await bot.close()

async def close():
    print("Closing on keyboard interrupt...")
    await shutdown()

async def on_connect():
    print(f" Connected to Discord (latency: {bot.latency*1000:,.0f} ms).")

async def on_resumed():
    print("Bot resumed.")

async def on_disconnect():
    print("Bot disconnected.")

@bot.event
async def on_message(message):
    pass

@bot.event
async def on_member_update(before, after):
    # if before.id in operatorlistcheck():
    #     if after.status != discord.Status.online:
    #         try:
    #             db = pymysql.connect(host=DB_IP,user=DB_USER,password=DB_PASS,database=DB_DB, port=DB_PORT,charset='utf8')
    #             c = db.cursor()
    #             setsupport = "UPDATE `oplist` SET `support_available` = %s WHERE `operator_id` = '%s'"
    #             c.execute(setsupport, (False, after.author.id))
    #             db.commit()
    #             db.close()
    #         except:
    #             pass
    channel = bot.get_channel(856678144122945558) #General-Chat Channel
    #channel2 = bot.get_channel(705381173970599966) #Staff Channel (Only staff)
    #channel3 = bot.get_channel(706425302187769926) #Boosters-only Channel
    
    #User boosted the server!
    if before.premium_since is None and after.premium_since is not None:
        #Check for existing user
        userexists = sparked_db.selectfirst("booster_id", "boosters", "booster_id", after.id)
        try:
            areyouhere = int(''.join(map(str, userexists)))
        except:
            areyouhere = 0
            pass
        if areyouhere == after.id:
            sparked_db.updateone("boosters", "isuserboosting", True, "booster_id", after.id)
        else:
            discord_name = after.name+"#"+after.discriminator
            sparked_db.insertonemaxthree("boosters", "booster_id","booster_name","isuserboosting", after.id, discord_name, True)

        #await channel3.send("{0.mention} Thanks for Server Boosting our server! You have been granted the role 'Server Booster' and you now have access to this channel and epic premium perks.\nYour information has been stored in our Database for gathering info.".format(after))
        await channel.send("<:nitrobooster:709992128440172606> {0.mention} just boosted the server! Let's celebrate! :partying_face:".format(after))

    #User stopped boosting :(
    elif before.premium_since is not None and after.premium_since is None:

        removeroleuser = sparked_db.selectfirst("boosroleinfo_id", "boosters", "booster_id", after.id)

        boosterappliedrole = int(''.join(map(str, removeroleuser)))
        await after.remove_roles(boosterappliedrole)

        sparked_db.updatetwo("boosters","isuserboosting", False, "isboostingrole", False, "booster_id", after.id)        

        #await channel3.send("{0.mention} Stopped boosting the server. Perks were removed and color roles were too. The user has not been removed to the database to keep information.".format(after))

#FINAL STATEMENTS
bot.run(mythicaltoken, reconnect=True) #Run the maximum token in a secret txt file