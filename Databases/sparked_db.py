#pylint: disable=unused-variable
#pylint: disable=unused-argument
#pylint: disable=W1401
#pylint: disable=F0401

from sqlite3 import connect
import discord
#import emoji #Used for the "-contest" command
import fwgconfig
import time
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

def dbchecklistap(bug_text):
    tempplaneslist = []
    msglinklist = []
    db, c = connectplz()
    checkforplanes = "SELECT * FROM `airplanelist` WHERE `airplane_name` LIKE %s LIMIT 5"
    c.execute(checkforplanes, ("%" + bug_text + "%",))
    wee = c.fetchall()
    similarplaneslist = [item[3] for item in wee]
    messagelinklist = [item[4] for item in wee]
    for allmyplanes in similarplaneslist:
        tempplaneslist.append(allmyplanes)
    for allmymsglinks in messagelinklist:
        msglinklist.append(allmymsglinks)
    return tempplaneslist, msglinklist

def hastimestamp(suggester):
    db, c = connectplz()
    checkfortimestamp = "SELECT `plsug_timeout` FROM `ginfo` WHERE `user_id` = '%s'"
    c.execute(checkfortimestamp, (suggester.id))
    wee = c.fetchone()
    if wee is None:
        #User has no timestamp, returns False
        return False
    else:
        #User has timestamp, return the timestamp
        return int(wee[0])

def createtimeout() -> int:
    tiempito = int(time.time())
    #Adds 30 days in timestamp
    tiempito = tiempito+2592000
    return tiempito

def planecooldown(suggester) -> str:
    actualtimeout = hastimestamp(suggester=suggester)
    return f"<t:{actualtimeout}>"

def toomanyplanes(suggester):
    db, c = connectplz()
    checkforsugg = "SELECT * FROM `airplanelist` WHERE `suggester_id` = %s"
    c.execute(checkforsugg, (suggester.id))
    wee = c.fetchall()
    userlist = [item[2] for item in wee]
    if len(userlist) >= 3:
        #Se ejecuta al no tener tiempo timeout
        if not hastimestamp(suggester=suggester):
            insertuser = "INSERT INTO `ginfo` (`user_id`,`user_name`,`plsug_timeout`) VALUES (%s,%s,%s)"
            timeout = int(createtimeout())
            c.execute(insertuser, (suggester.id, suggester.name, timeout))
            db.commit()
            db.close()
        #Se ejecuta cuando el timeout ya ha pasado o es igual
        elif hastimestamp(suggester=suggester) <= int(time.time()):
            updatestring = "UPDATE `airplanelist` SET `suggester_name` = %s WHERE `suggester_name` = %s"
            c.execute(updatestring, (f"{suggester.name} (UP)", suggester.name))
            updatestring2 = "UPDATE `ginfo` SET `plsug_timeout` = %s WHERE `user_id` = %s"
            c.execute(updatestring2, (createtimeout(), suggester.id))
            db.commit()
            db.close()
            return False

        return True
    else:
        return False


# def inserttoreportbug(thebot, author, channel, embed, embedmsg):
#     db, c = connectplz()
#     insertdata = "INSERT INTO `bug_reports` (`bot`,`author`,`channel`,`embed`,`embedmsg`) VALUES (%s,%s,%s,%s,%s)"
#     c.execute(insertdata, (thebot, author, channel, embed, embedmsg))
#     db.commit()
#     db.close()

# def checkreportbug():
#     db, c = connectplz()
#     selectdata = "SELECT `` FROM `bug_reports` WHERE `` = ''"

def mysql_table():
    db, c = connectplz()
    #Execute table for screenshot lists

    #This table should be edited manually everytime a new operator is added/removed.
    c.execute("""CREATE TABLE IF NOT EXISTS `oplist` (
                `rowid` INTEGER PRIMARY KEY AUTO_INCREMENT,
                `operator_id` BIGINT(16),
                `operator_name` VARCHAR(64),
                `join_time` LONGTEXT,
                `support_available` BOOLEAN,
                `power_level` INT(4)
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
                `airplane_name` VARCHAR(64),
                `message_link` VARCHAR(256)
                ) DEFAULT CHARSET=utf8;""")

    c.execute("""CREATE TABLE IF NOT EXISTS `ginfo` (
                `rowid` INTEGER PRIMARY KEY AUTO_INCREMENT,
                `user_id` BIGINT(16),
                `user_name` VARCHAR(64),
                `plsug_timeout` BIGINT(16)
                ) DEFAULT CHARSET=utf8;""")

    db.commit()
    db.close()

#SparkedDB means the connection specifically to Databases. (Where my bot is located and hosted)
class SparkedDB(commands.Cog):

    def __init__(self, bot):
        mysql_table()
        self.bot = bot

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

def setup(bot):
    bot.add_cog(SparkedDB(bot))