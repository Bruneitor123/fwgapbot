import discord
from discord.ext import commands
from discord.commands import slash_command
from discord.ui import Modal, InputText, Button, View, Select

noemoji = '<:no:862568274901991455>'
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
            max_length=400

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


    @slash_command()
    async def myairline(self,ctx):
        """This is specifically to configure your already existing airline..."""
        airline_existing = True
        if airline_existing:
            select2 = Select(placeholder="What do you want to configure?", options=[
            discord.SelectOption(label="Airline Description", description="Your airline description", emoji="<:fwg:769681026469068810>"),
            discord.SelectOption(label="Airline Alias", description="The airline acronym", emoji="<:plane:949433161081843762>"),
            discord.SelectOption(label="Airline Link", description="The discord server link for your airline", emoji="🎨"),
            discord.SelectOption(label="Bump Airline!", description="Bump your airline! Available only every 12hrs", emoji="⬆️"),
            discord.SelectOption(label="Cancel/Exit", description="", emoji=f"{noemoji}")])
            firstview = View()
            firstview.author = ctx.author.id

            async def new_callback(interaction):
                option = select2.values[0]
                firstview.clear_items()
                await ctx.interaction.edit_original_message(content='You have selected one already!',view=firstview)
                if option == "Airline Description":
                    return await interaction.response.send_message('You Chose Airline Desc!', ephemeral=True)
                elif option == "Airline Alias":
                    return await interaction.response.send_message('You Chose Airline Alias!', ephemeral=True)
                elif option == "Airline Link":
                    return await interaction.response.send_message('You Chose Airline Link!', ephemeral=True)
                elif option == "Bump Airline!":
                    return await interaction.response.send_message('You Chose Bump Airline!', ephemeral=True)
                elif option == "Cancel/Exit":
                    return await interaction.response.send_message('The Process has been cancelled! Use ``/reportbug`` again to start the command over.', ephemeral=True)

            select2.callback = new_callback
            #firstview.interaction_check = interaction_check
            firstview.add_item(select2)


            await ctx.respond('Click below to choose something!',view=firstview, ephemeral=True)


        else:
            return await ctx.respond('You don''t have an airline yet! You can try the ``/postairline`` command to register your airline here.', ephemeral=True)

        

def setup(bot):
    bot.add_cog(AirlinePost(bot))