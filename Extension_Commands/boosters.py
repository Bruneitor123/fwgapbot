#pylint: disable=unused-variable

import discord
import re
import asyncio
from discord.ext import commands
from discord import Color
from colormap import hex2rgb
import pymysql
import fwgconfig

DB_IP = fwgconfig.DATABASE_IP
DB_USER = fwgconfig.DATABASE_USER
DB_PASS = fwgconfig.DATABASE_PASSWORD
DB_DB = fwgconfig.DATABASE_DATABASE
DB_PORT = int(fwgconfig.DATABASE_PORT)

class boostersonly(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role('Moderator')
    async def boostcolor(self, ctx, target:discord.Member, hexcolor:str, *, color_name:str):
        """Give the user a Booster Color."""
        randomvar = 0

        ishex = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', hexcolor)
        if ishex: pass
        else: return await ctx.send('The color you are trying to use is NOT a valid Hex Color!')

        pos = 30 #29 Is the number where Server Booster is
        guild = ctx.guild
        isbooster = discord.utils.find(lambda r: r.name == 'Server Booster', ctx.message.guild.roles)
        if not isbooster in target.roles: return await ctx.send(f'The user {target.mention} is not a Server Booster!')
        r, g, b = hex2rgb(str(hexcolor))
        
        Tcolorname = ''.join(map(str, color_name))
        role = await guild.create_role(name=Tcolorname, colour=discord.Colour.from_rgb(r, g, b), hoist=False)
        db = pymysql.connect(host=DB_IP,user=DB_USER,password=DB_PASS,database=DB_DB, port=DB_PORT,charset='utf8')
        c = db.cursor()
        userboosted = "SELECT `booster_id` FROM `boosters` WHERE `booster_id` = '%s'"
        c.execute(userboosted, target.id)
        userexists = c.fetchone()
        try:
            areyouhere = int(''.join(map(str, userexists)))
        except:
            areyouhere = 0
            pass
        if areyouhere == target.id:
            updatebooster = "UPDATE `boosters` SET `boostroleinfo_id` = '%s', `isuserboosting` = '%s' WHERE `booster_id` = '%s'"
            c.execute(updatebooster, (role.id, True, target.id))
            db.commit()
            db.close()
            randomvar = 0

        else:
            insertuser = "INSERT INTO `boosters` (`booster_id`,`booster_name`,`isuserboosting`) VALUES (%s, %s, %s)"
            discord_name = target.name+"#"+target.discriminator
            c.execute(insertuser, (target.id, discord_name, True))
            db.commit()
            db.close()
            randomvar = 1
        

        await asyncio.sleep(1.131459)
        await role.edit(position=pos)

        await target.add_roles(role)
        if randomvar == 0:
            return await ctx.send(f'Added the Role {role.name} to the user {target.mention} and stored their role in the database!')
        elif randomvar == 1:
            return await ctx.send(f'The user {target.mention} was not stored in our database earlier! Our intelligence bots just worked that out.\nAdded the Role {role.name} to the user {target.mention} and stored their role in the database!')



if __name__ != "__main__":
        print('Booster Only commands are ready!')

def setup(bot):
    bot.add_cog(boostersonly(bot))