import discord
from discord.ext import commands
from discord.commands import slash_command, Option

#Prepare everything for the faq command:

#   TODO
#   -> Add a /faq command
#   -> command will use paginators and dropdowns to select game, then show many answers
#   -> Bot can forward people to tickets in case of no answer found.
#   -> Suggestions can be added to the faq via another command (Will change pre-defined answers and they will be stored in the database)

class FAQ(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        @slash_command()
        async def faq(self, ctx):
            pass

def setup(bot):
    bot.add_cog(FAQ(bot))