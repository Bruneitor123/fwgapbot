#pylint: disable=unused-variable
#pylint: disable=unused-argument
#pylint: disable=W1401
#pylint: disable=F0401

import discord
#Database Entries and More
from Databases import sparked_db
from discord.utils import find

#BOTTOM WILL DEBUG EVERY ASYNC TASK THAT HAPPENS (YES YES SIR)
#os.environ["PYTHONASYNCIODEBUG"] = "1"


description = '''The Private Multi-task Fat Whales Games Bot\n Made by MrBrunoh. (Version 3.0 Stable - Now this bot works only on Airplane Simulator)'''
bot = discord.Bot(description=description, intents=discord.Intents.all(), debug_guilds=[856678143608094751, 645052129710571581])
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
              "Fun_Commands.misc_commands",
              "Fun_Commands.TTT",
              "Fun_Commands.minesweeper",
              #Load extension_commands because i'd like to separate each one of those lol
              "Extension_Commands.reportbug",
              "Extension_Commands.suggest",
              "Extension_Commands.suggestplanes",
              
              ]

for extension in extensions:
        try:
            bot.load_extension(extension, store=False)
            print(f'Loaded {extension} correctly!')
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print(f'Failed to load extension {extension}\n{exc}')

@bot.slash_command()
@discord.default_permissions(administrator=True,)
async def reloadcog(ctx, *, cog:str):
    """Use only for admins. (RELoads a cog)"""
    try:
        bot.unload_extension(cog)
        bot.load_extension(cog)
        print(f'{cog} reloaded successfully!')
    except Exception as e:
        await ctx.send('{}: {}'.format(type(e).__name__, e))
    else:
        await ctx.send(f'Cog {cog} reloaded successfully!')

@bot.slash_command()
@discord.default_permissions(administrator=True,)
async def loadcog(ctx, *, cog:str):
    """Use only for admins. (Loads a cog)"""
    try:
        bot.load_extension(cog)
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        await ctx.respond(f'Failed to load extension {cog}\n{exc}')
    else:
        await ctx.respond(f'Cog {cog} lock n'' loaded successfully!')


@bot.event
async def on_ready():
    #Wait until the bot has loaded into discord
    await bot.wait_until_ready()

    #Set a cool presence, why not?

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.users)} users in {len(bot.guilds)} guilds."))

    print(" /\-----------------------------------------------------------------------------------------/\ ")
    print('                                         Logged in as:')
    print(f"                                    {bot.user.name}#{bot.user.discriminator}")
    print(f'                            Watching {len(bot.users)} users in {len(bot.guilds)} guilds')
    print(f'                            Latest known bot latency is: {bot.latency*1000:,.0f} ms')
    print(" /\------------------------------- Bot is ready and running! -------------------------------/\ ")

@bot.event
async def on_member_update(before, after):
    channel = find(lambda x:x.name == '💬lounge', after.guild.text_channels) #General-Chat Channel
    
    #User boosted the server!
    if before.premium_since is None and after.premium_since is not None:
        #Check for existing user
        userexists = sparked_db.selectfirst("booster_id", "boosters", "booster_id", after.id)
        try:
            areyouhere = int(''.join(map(str, userexists)))
        except:
            areyouhere = 0
        if areyouhere == after.id:
            sparked_db.updateone("boosters", "isuserboosting", True, "booster_id", after.id)
        else:
            discord_name = after.name+"#"+after.discriminator
            sparked_db.insertonemaxthree("boosters", "booster_id","booster_name","isuserboosting", after.id, discord_name, True)

        #await channel3.send("{0.mention} Thanks for Server Boosting our server! You have been granted the role 'Server Booster' and you now have access to this channel and epic premium perks.\nYour information has been stored in our Database for gathering info.".format(after))
        await channel.send("<:nitrobooster:709992128440172606> {0.mention} just boosted the server! Let's celebrate! :partying_face:".format(after))

    #User stopped boosting :(
    elif before.premium_since is not None and after.premium_since is None:

        #removeroleuser = sparked_db.selectfirst("boosroleinfo_id", "boosters", "booster_id", after.id)
        #boosterappliedrole = int(''.join(map(str, removeroleuser)))
        #await after.remove_roles(boosterappliedrole)

        sparked_db.updatetwo("boosters","isuserboosting", False, "isboostingrole", False, "booster_id", after.id)        

        await channel.send("{0.mention} Stopped boosting the server. Perks were removed and color roles were too. The user has not been removed to the database to keep information.".format(after))


#FINAL STATEMENTS
bot.run(mythicaltoken, reconnect=True) #Run the maximum token in a secret txt file