#pylint: disable=unused-variable
#pylint: disable=unused-argument
#pylint: disable=W1401
#pylint: disable=F0401

from sqlite3 import connect
import discord
#import emoji #Used for the "-contest" command
import fwgconfig
import emoji
import pymysql #PyMySQL is our system to connect Python to various Databases
from discord.ext import commands
from discord.commands import slash_command
#from PIL import Image #Used for the "-contest" command

DB_IP = fwgconfig.DATABASE_IP
DB_USER = fwgconfig.DATABASE_USER
DB_PASS = fwgconfig.DATABASE_PASSWORD
DB_DB = fwgconfig.DATABASE_DATABASE
DB_PORT = int(fwgconfig.DATABASE_PORT)

def connectplz():
    db = pymysql.connect(host=DB_IP,user=DB_USER,password=DB_PASS,database=DB_DB, port=DB_PORT,charset='utf8')
    c = db.cursor()
    return db, c;

def operatorlistcheck():
    db, c = connectplz()

    c.execute("SELECT `operator_id` FROM `oplist`")
    wee = c.fetchall()
    oplist = [item[0] for item in wee]
    nodupelist = list(dict.fromkeys(oplist))
    return nodupelist

def selectfirst(first, second, third, fourth):
    db, c = connectplz()

    selectstring = "SELECT `%s` FROM `%s` WHERE `%s` = '%s'"
    c.execute(selectstring, first, second, third, fourth)
    fetchfirst = c.fetchone()
    return fetchfirst

def updateone(first, second, third, fourth, fifth):
    db, c = connectplz()

    updatestring = "UPDATE `%s` SET `%s` = %s WHERE `%s` = '%s'"
    c.execute(updatestring, (first, second, third, fourth, fifth))
    db.commit()
    db.close()

def updatetwo(first, second, third, fourth, fifth, sixth, seventh):
    db, c = connectplz()

    updatestringtwo = "UPDATE `%s` SET `%s` = '%s', `%s` = '%s' WHERE `%s` = '%s'"
    c.execute(updatestringtwo, (first, second, third, fourth, fifth, sixth, seventh))
    db.commit()
    db.close()

def insertonemaxthree(first, second, third, fourth, fifth, sixth, seventh):
    db, c = connectplz()
    if fourth is None:
        pass
    if sixth is None:
        pass
    insertuser = "INSERT INTO `%s` (`%s`,`%s`,`%s`) VALUES (%s, %s, %s)"
    c.execute(insertuser, (first, second, third,fourth,fifth, sixth, seventh))
    db.commit()
    db.close()

# def inserttoreportbug(thebot, author, channel, embed, embedmsg):
#     db, c = connectplz()
#     insertdata = "INSERT INTO `bug_reports` (`bot`,`author`,`channel`,`embed`,`embedmsg`) VALUES (%s,%s,%s,%s,%s)"
#     c.execute(insertdata, (thebot, author, channel, embed, embedmsg))
#     db.commit()
#     db.close()

# def checkreportbug():
#     db, c = connectplz()
#     selectdata = "SELECT `` FROM `bug_reports` WHERE `` = ''"

#Start Database for Screenshot Contest (Old?)
def mysql_table():
    db, c = connectplz()
    #Execute table for screenshot lists
    c.execute("""CREATE TABLE IF NOT EXISTS `sslist` (
                `rowid` INTEGER PRIMARY KEY AUTO_INCREMENT,
                `discord_id` BIGINT(16),
                `discord_name` VARCHAR(64),
                `screenshots` INT(4)
                ) DEFAULT CHARSET=utf8;""")

    c.execute("""CREATE TABLE IF NOT EXISTS `giveawaysrv` (
                `rowid` INTEGER PRIMARY KEY AUTO_INCREMENT,
                `giveaway_id` BIGINT(64),
                `timedelta_left` INT(8),
                `winner_id` BIGINT(64),
                `winner_name` VARCHAR(64)
                ) DEFAULT CHARSET=utf8; """)

    c.execute("""CREATE TABLE IF NOT EXISTS `giveawaycfg` (
                `rowid` INTEGER PRIMARY KEY AUTO_INCREMENT,
                `g_time` INT(8),
                `g_channel` VARCHAR(64),
                `g_message` LONGTEXT,
                `g_prize` LONGTEXT,
                `g_emoji` VARCHAR(64)
                ) DEFAULT CHARSET=utf8;""")

    #This table should be edited manually everytime a new operator is added/removed.
    c.execute("""CREATE TABLE IF NOT EXISTS `oplist` (
                `rowid` INTEGER PRIMARY KEY AUTO_INCREMENT,
                `operator_id` BIGINT(16),
                `operator_name` VARCHAR(64),
                `join_time` LONGTEXT,
                `support_available` BOOLEAN,
                `power_level` INT(4)
                ) DEFAULT CHARSET=utf8;""")

    c.execute("""CREATE TABLE IF NOT EXISTS `dmsupport` (
                `rowid` INTEGER PRIMARY KEY AUTO_INCREMENT,
                `supportuser_id` BIGINT(16),
                `supportuser_name` VARCHAR(64),
                `isuserticketing` BOOLEAN,
                `channelusinguser` BIGINT(16),
                `staffuser_id` BIGINT(16)
                ) DEFAULT CHARSET=utf8;""")
    
    c.execute("""CREATE TABLE IF NOT EXISTS `boosters` (
                `rowid` INTEGER PRIMARY KEY AUTO_INCREMENT,
                `booster_id` BIGINT(16),
                `booster_name` VARCHAR(64),
                `isuserboosting` BOOLEAN,
                `isboostingrole` BOOLEAN,
                `boostroleinfo_id` BIGINT(24)
                ) DEFAULT CHARSET=utf8;""")

    c.execute("""CREATE TABLE IF NOT EXISTS `airplanelist` (
                `rowid` INTEGER PRIMARY KEY AUTO_INCREMENT,
                `suggester_id` BIGINT(16),
                `suggester_name` VARCHAR(64),
                `airplane_name` VARCHAR(32),
                `message_link` VARCHAR(128)
                ) DEFAULT CHARSET=utf8;""")

#SparkedDB means the connection specifically to ONLY SparkedHosting Databases. (Where my bot is located and hosted)
class SparkedDB(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        mysql_table()

    @slash_command()
    async def operatorlist(self, ctx):
        """A Command that gathers every staff member stored in a database, returns an embed with a list."""
        db, c = connectplz()
        level1list = []
        level2list = []
        level3list = []
        level4list = []

        c.execute("SELECT `operator_id` FROM `oplist` WHERE `power_level` = 1")
        wee = c.fetchall()
        idlistlvl1 = [item[0] for item in wee]
        for id_ in idlistlvl1:
            level1list.append(discord.utils.get(ctx.guild.members, id=id_).mention)
        c.execute("SELECT `operator_id` FROM `oplist` WHERE `power_level` = 2")
        wee = c.fetchall()
        idlistlvl2 = [item[0] for item in wee]
        for id_ in idlistlvl2:
            level2list.append(discord.utils.get(ctx.guild.members, id=id_).mention)
        c.execute("SELECT `operator_id` FROM `oplist` WHERE `power_level` = 3")
        wee = c.fetchall()
        idlistlvl3 = [item[0] for item in wee]
        for id_ in idlistlvl3:
            level3list.append(discord.utils.get(ctx.guild.members, id=id_).mention)
        c.execute("SELECT `operator_id` FROM `oplist` WHERE `power_level` = 4")
        wee = c.fetchall()
        idlistlvl4 = [item[0] for item in wee]
        for id_ in idlistlvl4:
            level4list.append(discord.utils.get(ctx.guild.members, id=id_).mention)


        #Level 1 = Trial Moderators
        #Level 2 = Official Moderators
        #Level 3 = Administrators
        #Level 4 = Super Administrators
        embed=discord.Embed(title="FWG OPList", description=emoji.emojize(" :shield: Operators List"), color=0xFFFFFF)
        embed.set_author(name=self.bot.user, icon_url=self.bot.user.avatar.url)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/707431044902682644/931755527334137886/Logo4_AS_copy.png")
        if level1list == []:
            embed.add_field(name="Level 1 (TM)", value="No newbie moderators.", inline=True)
        else:
            embed.add_field(name="Level 1 (TM)", value="\n".join(level1list), inline=True)
        embed.add_field(name="Level 2 (OM)", value="\n".join(level2list), inline=True)
        if level3list == []:
            embed.add_field(name="Level 3 (ADM)", value="No admins", inline=True)
        else:
            embed.add_field(name="Level 3 (ADM)", value="\n".join(level3list), inline=True)
        embed.add_field(name="Level 4 (SADM)", value="\n".join(level4list), inline=True)
        #embed.set_footer(text="This message will be deleted on 60 seconds.")
        await ctx.respond(embed=embed)


    # @commands.command()
    # async def contest(self, ctx, participate = None):
    #     """Contest Command for screenshots contest."""
    #     userboi = ctx.author
    #     themessage = ctx.message
    #     #Contest Ended
    #     await themessage.delete()
    #     if 1 == 2:
    #         return await ctx.send(f'The contest has ended. Total participants were: 125! Wow!', delete_after=10.0)
    #     else:
    #         return await ctx.send(f'The contest has ended. Total participants were: 125! Wow!', delete_after=10.0)

    #     #Forces Return to no longer accept requests into our contest. (Below we have an intended warning)
    #     emoji1 = '<:yes:724011319841390592>'
    #     emoji2 = '<:no:724011319887396915>'
    #     #Check if user wants to participate
    #     if participate == 'go':
    #         if len(ctx.message.attachments) > 0:
    #             surek = await ctx.send("Are you sure to participate in the Screenshot contest with that image?")
    #             await surek.add_reaction(emoji1)
    #             await surek.add_reaction(emoji2)
    #             def check(reaction, user):
    #                 return user == userboi and str(reaction.emoji) in ['<:yes:724011319841390592>', '<:no:724011319887396915>']
    #             try:
    #                 reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
    #             except asyncio.TimeoutError:
    #                 await surek.delete()
    #                 await themessage.delete()
    #                 return
    #             else:
    #                 if str(reaction.emoji) == '<:yes:724011319841390592>':
    #                     await surek.delete()
    #                     yes = await ctx.send('Continuing... (This may take a while)', delete_after=5.0)
    #                     pass
    #                 elif str(reaction.emoji) == '<:no:724011319887396915>':
    #                     await surek.delete()
    #                     await themessage.delete()
    #                     return
    #             epicurl = ctx.message.attachments[0]
    #             async with aiohttp.ClientSession() as session:
    #                     async with session.get(epicurl.url) as resp:
    #                         if resp.status != 200:
    #                             return await ctx.send('Could not download file...')
    #                         data = io.BytesIO(await resp.read())
    #             try:
    #                 with Image.open(data) as image_pil:
    #                     pass
    #                     #Nice!
    #                     #DO nothing
    #             except (Image.DecompressionBombError, Image.DecompressionBombWarning) as e:
    #                 cyberlog = self.bot.get_channel(727186902498672710)
    #                 await cyberlog.send(f'User {userboi} sent a potentially malicious file. Sending traceback:')
    #                 await cyberlog.send(e)
    #                 return await ctx.send('Potential Malicious File detected. Please try again.', delete_after=10.0)
    #             except:
    #                 await asyncio.sleep(1)
    #                 await themessage.delete()
    #                 return await ctx.send('Unsupported file type! Remember to use an ``Image file`` format when attaching. (Gifs are **not** allowed)', delete_after=10.0)
    #             data.seek(0)
    #             secretchannel = self.bot.get_channel(725813797935251478) #Get the bug-report-images channel located in Bruno's Spaceship
    #             uploaded_filename_message = await secretchannel.send(f"{userboi} Sent this! (Screenshot Contest)", file=discord.File(data, filename=epicurl.filename))
    #             data.close()
    #             uploaded_filename_url = uploaded_filename_message.attachments[0].url
    #             await themessage.delete()
    #             #Set the image from Bruno's Spaceship to the embed
    #             embed1=discord.Embed(title=emoji.emojize("FWG Screenshot Contest"), description=" ", color=0xFFFFFF)
    #             embed1.set_author(name=userboi, icon_url=userboi.avatar.url)
    #             embed1.set_thumbnail(url="https://cdn.discordapp.com/attachments/707431044902682644/931755527334137886/Logo4_AS_copy.png")
    #             embed1.set_image(url=uploaded_filename_url)
    #             channel = self.bot.get_channel(725809209471664420)
    #             discord_name = userboi.name+"#"+userboi.discriminator
    #             db = pymysql.connect(host=DB_IP,user=DB_USER,password=DB_PASS,database=DB_DB, port=DB_PORT,charset='utf8')
    #             c = db.cursor()
    #             c.execute("SELECT discord_id FROM sslist")
    #             wee = c.fetchall()
    #             thisalist = [item[0] for item in wee]
    #             secretchannel2 = self.bot.get_channel(726837031803551824)
    #             if userboi.id in thisalist:
    #                 pass
    #             else:
    #                 sql = "INSERT INTO `sslist` (`discord_id`, `discord_name`) VALUES (%s, %s)"
    #                 await secretchannel2.send(f"{sql}" % (userboi.id, discord_name))
    #                 try:
    #                     c.execute(sql, (userboi.id, discord_name))
    #                     db.commit()
    #                 except pymysql.err.InternalError:
    #                     return await ctx.send('An Internal Error ocurred, this is most likely because your username contains special characters.', delete_after=10.0)
    #             lol = "SELECT screenshots FROM sslist WHERE `discord_id` = '%s'"
    #             await secretchannel2.send(f"{lol}" % userboi.id)
    #             c.execute(lol, userboi.id)
    #             check23 = c.fetchone()
    #             res = ''.join(map(str, check23))
    #             if res == 'None':
    #                 screenshots = 1
    #                 sql2 = "UPDATE `sslist` SET `screenshots` = %s WHERE `discord_id` = '%s'"
    #                 await secretchannel2.send(f"{sql2}" % (screenshots, userboi.id))
    #                 c.execute(sql2, (screenshots, userboi.id))
    #             elif int(res) >= 1:
    #                 if int(res) >= 3:
    #                     return await ctx.send('You have reached the limit of 3 images! Thanks for participating.', delete_after=10.0)
    #                 screenshots = int(res)+1
    #                 sql2 = "UPDATE `sslist` SET `screenshots` = %s WHERE `discord_id` = '%s'"
    #                 await secretchannel2.send(f"{sql2}" % (screenshots, userboi.id))
    #                 c.execute(sql2, (screenshots, userboi.id))
    #             db.commit()
    #             db.close()
    #             sendembed1 = await channel.send(embed=embed1)
    #             await sendembed1.add_reaction('🌟')
    #             return
    #         elif len(ctx.message.attachments) > 1:
    #             await themessage.delete()
    #             return await ctx.send('Only 1 image is allowed per command, if you want to attach more images, please use the command again.', delete_after=10.0)
    #         else:
    #             await themessage.delete()
    #             return await ctx.send('You need to attach an image to participate!', delete_after=8.0)
    #     embed=discord.Embed(title=emoji.emojize("FWG Screenshot Contest"), description=" ", color=0xFFFFFF)
    #     embed.set_author(name=userboi, icon_url=userboi.avatar.url)
    #     embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/707431044902682644/931755527334137886/Logo4_AS_copy.png")
    #     embed.add_field(name="How to Participate?", value=(emoji.emojize("React with :tada: to get a guide on how to participate.")), inline=True)
    #     embed.add_field(name="Contest Rules", value=(emoji.emojize("React with :book: to watch all the rules for the screenshot contest.")), inline=True)
    #     sendembed = await ctx.send(embed=embed)
    #     await themessage.delete()
    #     await sendembed.add_reaction('🎉')
    #     await sendembed.add_reaction('📖')
    #     await sendembed.add_reaction('❌')
    #     def check2(reaction, user):
    #         return user == userboi and str(reaction.emoji) in ['🎉', '📖', '❌']
    #     try:
    #         reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check2)
    #     except asyncio.TimeoutError:
    #         await sendembed.delete()
    #         return
    #     else:
    #         if str(reaction.emoji) == '🎉':
    #             await sendembed.delete()
    #             embed2=discord.Embed(title=emoji.emojize("FWG Screenshot Contest"), description=" ", color=0xFFFFFF)
    #             embed2.set_author(name="Screenshot Contest - Participation", icon_url=userboi.avatar.url)
    #             embed2.set_thumbnail(url="https://cdn.discordapp.com/attachments/707431044902682644/931755527334137886/Logo4_AS_copy.png")
    #             embed2.add_field(name="Participation", value=(emoji.emojize("In order to participate, use: ``-contest go`` (Case Sensitive, you must type the command as it is)")), inline=False)
    #             embed2.add_field(name="How would the command work?", value=(emoji.emojize("Just simply type the command, while attaching a real image to the command (message).")), inline=False)
    #             embed2.add_field(name="Image Allowed Formats", value=(emoji.emojize("Our allowed formats to send an image are all kind of images that your PC would allow.")), inline=False)
    #             embed2.set_footer(text="This Message will be deleted in 30 Seconds.")
    #             sendembed2 = await ctx.send(embed=embed2, delete_after=30.0)
    #         elif str(reaction.emoji) == '📖':
    #             await sendembed.delete()
    #             embed3=discord.Embed(title=emoji.emojize("FWG Screenshot Contest"), description=" ", color=0xFFFFFF)
    #             embed3.set_author(name="Screenshot Contest - Rules", icon_url=userboi.avatar.url)
    #             embed3.set_thumbnail(url="https://cdn.discordapp.com/attachments/707431044902682644/931755527334137886/Logo4_AS_copy.png")
    #             embed3.add_field(name="Summary:", value=(emoji.emojize("Rules are simple:\n- 3 Screenshots Max per person\n - Image must be a screenshot from Airport Tycoon\n - Do not steal others' screenshots and claim them as yours\n - No editing/photoshop allowed, except image cropping.\n - Only images are allowed, no GIFs or video files.")), inline=False)
    #             embed3.set_footer(text="This Message will be deleted in 30 Seconds.")
    #             sendembed3 = await ctx.send(embed=embed3, delete_after=30.0)
    #         elif str(reaction.emoji) == '❌':
    #             await sendembed.delete()

def setup(bot):
    bot.add_cog(SparkedDB(bot))