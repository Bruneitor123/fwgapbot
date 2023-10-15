import discord
from Databases import sparked_db
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
            label="Enter your Airline Description",
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


        #stores message id, with data; also stores user id who posted it
        msg = await interaction.response.send_message(embed=embed, view=view)
        db, c = sparked_db.connectplz()
        insertuser = "INSERT INTO `airlines` (`msg_id`,`owner_id`,`airline_name`,`airline_alias`,`discord_link`,`airline_desc`) VALUES (%s, %s, %s, %s, %s, %s)"
        c.execute(insertuser, (msg.id, interaction.user.id, self.children[0].value, self.children[1].value, self.children[2].value, self.children[3].value))
        updatestring = "UPDATE `airlines` SET `is_airline_active` = True WHERE `owner_id` = '%s'"
        c.execute(updatestring, (interaction.user.id))
        db.commit()
        db.close()
        #then do below
        await interaction.followup.send('Airline Posted!', ephemeral=True)


class AirlinePost(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def postairline(self,ctx):
        #TODO: checks if user has airline to prevent command usage/spam
        """This will post your airline in the airlines channel."""
        modal = DetModal(title="Submit an Airline Form", bot=self.bot)
        await ctx.send_modal(modal)


    @slash_command()
    async def myairline(self,ctx):
        """This is specifically to configure your already existing airline..."""
        #gets airline_existing wiht user id, if airline posted then will get info and prepare everything
        airline_existing = sparked_db.existing_airline(ctx.author.id)
        if airline_existing:
            select2 = Select(placeholder="What do you want to configure?", options=[
            #airline desc is literally the first embed with desc
            discord.SelectOption(label="Airline Description", description="Your airline description", emoji="<:fwg:769681026469068810>"),
            #airline alias it the max 4 characters for the external link
            discord.SelectOption(label="Airline Alias", description="The airline acronym", emoji="<:plane:949433161081843762>"),
            #airline link for the external link (must be discord.gg)
            discord.SelectOption(label="Airline Link", description="The discord server link for your airline", emoji="🎨"),
            #bump airline will delete the latest message (using id and fetchmessage), then it will grab same data from before and re-post it. literally bumping it
            discord.SelectOption(label="Bump Airline!", description="Bump your airline! Available only every 12hrs", emoji="⬆️"),
            #exits
            discord.SelectOption(label="Cancel/Exit", description="", emoji=f"{noemoji}")])
            firstview = View()
            firstview.author = ctx.author.id

            async def new_callback(interaction):
                db, c = sparked_db.connectplz()
                selectsystem = "SELECT %s FROM airlines WHERE owner_id = '%s'"
                option = select2.values[0]
                firstview.clear_items()
                await ctx.interaction.edit_original_message(content='You have selected one already!',view=firstview)
                if option == "Airline Description":
                    c.execute(selectsystem, ('airline_desc', interaction.user.id))
                    airdesc = c.fetchone()
                    await interaction.response.send_message(f'Your Airline Description currently is: \n{airdesc}', ephemeral=True)

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