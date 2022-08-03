#pylint: disable=unused-variable

import discord
import random
import aiohttp
from discord.ext import commands
from discord.commands import slash_command, Option
from discord.commands import SlashCommandGroup

class Miscellaneous(commands.Cog):
    
    def __init__(self, bot_: discord.Bot):
        self.bot = bot_

    fun = SlashCommandGroup("fun", "Commands dedicated, to... Have fun.")

    @fun.command()
    async def add(self, ctx, left: int, right: int):
        """Adds two numbers together like a sum."""
        if left >= 10000:
            await ctx.respond('Too much math.', ephemeral=True)
            return
        elif right >= 10000:
            await ctx.respond('Too much math.', ephemeral=True)
            return
        await ctx.respond(left + right)

    @fun.command()
    async def roll(self, ctx, dice: str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
            if rolls >= 35:
                await ctx.respond('Too much to solve.', ephemeral=True)
                return
            elif limit >= 35:
                await ctx.respond('Too much to solve.', ephemeral=True)
                return
        except Exception:
            await ctx.respond('Format has to be in NdN (NumberdNumber) (1d10)!', ephemeral=True)
            return
        result = [random.randint(1, limit) for r in range(rolls)]
        total = 0
        for x in result:
            total = total + x
        result = [str(result) for result in result]
        await ctx.respond(", ".join(result) + "\n Or the total sum: **{0}**".format(str(total)))

    @fun.command()
    async def joined(self, ctx, member: discord.Member):
        """Says when a member joined."""
        await ctx.respond('{0.name} joined in {0.joined_at}'.format(member))

    @fun.command()
    async def cat(self, ctx):
        """Get a random cat image from The Cat API."""
        search_url = 'https://api.thecatapi.com/v1/images/search'
        search_headers = None

        async with aiohttp.ClientSession() as session:
            async with session.get(search_url, headers=search_headers) as resp:
                json_resp = await resp.json()
        
        cat_dict = json_resp[0]
        cat_img_url = cat_dict['url']

        await ctx.respond(f'{cat_img_url}')

    @fun.command()
    async def dog(self, ctx):
        """Get a random dog image from The Dog API."""
        search_url = 'https://api.thedogapi.com/v1/images/search'
        search_headers = None

        async with aiohttp.ClientSession() as session:
            async with session.get(search_url, headers=search_headers) as resp:
                json_resp = await resp.json()
        
        dog_dict = json_resp[0]
        dog_img_url = dog_dict['url']

        await ctx.respond(f'{dog_img_url}')

    @fun.command()
    async def magic8ball(self, ctx):
        """Decide your fate via this Magic 8 Ball..."""
        return await ctx.respond(random.choice([
            "Probably.", "Perhaps.", "This won't work.", "Ask Again Later!", "This answer was censored because reasons", "Yeah!", "It will do!", "Why NOT?!", "Of course!",
            "Derp", "In your dreams", "It will be done.", "Yup", "No.", "Yes.", "YES, YES YES.", "My reply is a yes.", "My Reply is a no.", "Cringe..."]))

    #Totally Random Thing
    @slash_command()
    @discord.default_permissions(administrator=True,)
    async def say(self, ctx, 
    sayso: Option(str, "What's the secret message, chief?"),
    attachment: Option(discord.Attachment, description="Attach a file if you want, this is optional.", required=False)
    ):
        """Let the bot say whatever you want."""
        if attachment:
            file = await attachment.to_file()
            sentowo = await ctx.send('{0}'.format(sayso), file=file)
        else:
            sentowo = await ctx.send('{0}'.format(sayso))
        await ctx.respond(f'This message was sent successfully!', ephemeral=True)

    @slash_command()
    @discord.default_permissions(administrator=True,)
    async def secretsay(self, ctx, 
    channel: Option(discord.TextChannel, "Select a channel for input."), 
    sayso: Option(str, "What's the message you want to send anonymously?"),
    attachment: Option(discord.Attachment, description="Attach a file if you want, this is optional.", required=False)
    ):
        """Admin Only Command."""
        if attachment:
            file = await attachment.to_file()
            sentowo = await channel.send('{0}'.format(sayso), file=file)
        else:
            sentowo = await channel.send('{0}'.format(sayso))
        await ctx.respond(f'The message was sent successfully! [Check it out!]({sentowo.jump_url})', ephemeral=True)

    @fun.command()
    async def ping(self, ctx):
        """Pong!"""
        finallatency = self.bot.latency*10**3
        await ctx.respond("Pong! ``{}ms``".format(round(finallatency, 1)))

def setup(bot):
    bot.add_cog(Miscellaneous(bot))
