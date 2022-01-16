#pylint: disable=unused-variable

import discord
import time
from datetime import datetime, timezone
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        """This is a help command."""
        actualTitle = 'Fat Whale Game Command List'
        nowtime = time.time()
        embed = discord.Embed(color=0x0040ff,title=actualTitle, url="https://fatwhalegames.com/", timestamp=datetime.fromtimestamp(nowtime, tz=timezone.utc))
        embed.add_field(name='Most Used Commands', value='*-reportbug* -> (New!) Interactive command to report bugs easily.\n*-suggest*   -> Suggests something in the suggestions channel.\n*-help*      -> Shows this message', inline=False)
        embed.add_field(name='Other Value', value='*-randomcommand* -> Do something', inline=False)
        embed.set_footer(text=f"Amazing Cool Super Hiper Developed Bot", icon_url='https://cdn.discordapp.com/attachments/707431044902682644/766476888234262541/FWG_BlueLogo.png')
        return await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))