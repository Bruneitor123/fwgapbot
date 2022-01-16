import discord
import emoji
from discord.ext import commands
from discord.ui import Button, View

class AdminCMDS(commands.Cog):


    def __init__(self, bot):
        self.bot = bot


    @commands.command(hidden=True)
    @commands.is_owner()
    async def createembed(self, ctx):

        embed=discord.Embed(title="Official RP Roblox Server", description=emoji.emojize("Roleplay with others as a pilot or crew in our official RP server. \n\n Make sure your [Privacy Settings](https://www.roblox.com/my/account#!/privacy) are set to 'Everyone' can invite you!"), color=0x00FF00)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/707431044902682644/931755527334137886/Logo4_AS_copy.png")
        embed.set_footer(text="Server is Active and Running!", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Eo_circle_green_checkmark.svg/512px-Eo_circle_green_checkmark.svg.png")
        embed.set_image(url="https://cdn.discordapp.com/attachments/707431044902682644/931756352420868116/Trello_Background.png")

        button = Button(label="Play Now", style=discord.ButtonStyle.url, url="https://www.roblox.com/games/6938764986?privateServerLinkCode=71324364136063014884230263882021", emoji="<:doge:921427172730748994>")

        view = View(timeout=None)
        view.add_item(button)
        
        await ctx.send(embed=embed, view=view)

def setup(bot):
    bot.add_cog(AdminCMDS(bot))