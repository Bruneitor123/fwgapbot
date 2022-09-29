import discord
from discord.ext import commands
from discord.commands import slash_command
from discord.ui import Modal, InputText
from Databases import sparked_db

class DetModal(Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

        self.add_item(InputText(
            label= "Enter your Airline Name",
            placeholder= "Fat Whale gAAAMES",
            style=discord.InputTextStyle.short
        ))

        self.add_Item(InputText(
            label="Enter your Discord/Group invite link",
            placeholder="https://discord.gg/FWG",
            style=discord.InputTextStyle.singleline
        ))

        self.add_Item(InputText(
            label="Enter your Airline Description",
            placeholder="Welcome to Fat Whale Games! This server...",
            style=discord.InputTextStyle.paragraph
        ))

    async def callback(self, interaction:discord.Interaction):
        embed = discord.Embed(title="", colour=discord.Colour.blue)
        embed.add_field(name="Airline Name", value=self.children[0].value, inline=False)
        embed.add_field(name="Discord Link", value=self.children[1].value, inline=False)
        embed.add_field(name="Airline Descreiption", value=self.children[2].value, inline=False)
        await interaction.response.send_message(embed=embed)


class AirlinePost(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @slash_command
    async def postairline(self, ctx):
        """This will post your airline in the airlines channel."""
        modal = DetModal(title="Submit an Airline Form")
        await ctx.send_modal(modal)

def setup(bot):
    bot.add_cog(AirlinePost(bot))