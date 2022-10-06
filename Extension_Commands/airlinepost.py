import discord
from discord.ext import commands
from discord.commands import slash_command
from discord.ui import Modal, InputText, Button, View

class DetModal(Modal):
    def __init__(self, bot, *args, **kwargs):
        self.bot = bot
        super().__init__(*args,**kwargs)

        self.add_item(InputText(
            label= "Enter your FULL Airline Name",
            placeholder= "Fat Whale Games",
            style=discord.InputTextStyle.short,
            min_length=7
        ))

        self.add_item(InputText(
            label= "Enter the Airline Alias",
            placeholder= "FWG",
            style=discord.InputTextStyle.short,
            max_length=4
        ))

        self.add_item(InputText(
            label="Enter your Discord/Group invite link",
            placeholder="https://discord.gg/FWG",
            style=discord.InputTextStyle.short,
            max_length=30
        ))

        self.add_item(InputText(
            label="Enter your Airline Short Description",
            placeholder="Welcome to Fat Whale Games! This server contains...",
            style=discord.InputTextStyle.long,
            min_length=50,
            max_length=200

        ))

    async def callback(self, interaction:discord.Interaction):
        embed = discord.Embed(title=f"{self.children[0].value} - Server", color=0xFFFFFF)
        invite = await self.bot.fetch_invite(url=self.children[2].value, with_counts=True)
        embed.add_field(name="\u200b", value=self.children[3].value, inline=False)
        iconurl = f"{invite.guild.icon}"
        embed.set_thumbnail(url=iconurl)
        embed.set_footer(text=f"Server Members: {invite.approximate_member_count}")
        button = Button(label=f"Join {self.children[1].value} now!", style=discord.ButtonStyle.link, emoji="<a:rainbowstud:838540235440390174>", url=self.children[2].value)
        view = View()
        view.add_item(button)


        await interaction.response.send_message(embed=embed, view=view)
        await interaction.followup.send('Airline Posted!', ephemeral=True)


class AirlinePost(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def postairline(self,ctx):
        """This will post your airline in the airlines channel."""
        modal = DetModal(title="Submit an Airline Form", bot=self.bot)
        await ctx.send_modal(modal)

def setup(bot):
    bot.add_cog(AirlinePost(bot))