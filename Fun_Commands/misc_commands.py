#pylint: disable=unused-variable

import discord
import asyncio
import random
import aiohttp
from discord.ext import commands
from Databases import sparked_db
from discord.commands import slash_command

class Miscellaneous(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def add(self, ctx, left: int, right: int):
        """Adds two numbers together like a sum."""
        if left >= 10000:
            await ctx.respond('Too much math.', ephemeral=True)
            return
        elif right >= 10000:
            await ctx.respond('Too much math.', ephemeral=True)
            return
        await ctx.respond(left + right)

    @slash_command()
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

    @slash_command()
    async def choose(self, ctx, choices: str):
        """Chooses between multiple choices."""
        theauthor = ctx.author
        role = discord.utils.find(lambda r: r.name == 'Server Booster', ctx.message.guild.roles)
        if role in theauthor.roles:
            if len(choices) < 5:
                return await ctx.respond('A sentence must have at least 5 words.', ephemeral=True)
            li = list(choices.split(" "))
            await ctx.respond(random.choice(li))
        else:
            return await ctx.respond('Hey, you must be a Server Booster in order to use this command!', ephemeral=True)

    # @commands.command()
    # async def repeat(self, ctx, times: int, *, content='repeating...'):
    #     """Repeats a message multiple times."""
    #     theauthor = ctx.author
    #     role = discord.utils.find(lambda r: r.name == 'Server Booster', ctx.message.guild.roles)
    #     if role in theauthor.roles:
    #         for i in range(times):
    #             if times < 5:
    #                 await ctx.send(content)
    #             else:
    #                 return await ctx.send('Are you trying to spam?, Sorry, You can''t.', delete_after=10.0)
    #     else:
    #         return await ctx.send('Hey, you must be a Server Booster in order to use this command!', delete_after=10.0)

    @slash_command()
    async def joined(self, ctx, member: discord.Member):
        """Says when a member joined."""
        await ctx.respond('{0.name} joined in {0.joined_at}'.format(member))

    @slash_command()
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

    @slash_command()
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

    @slash_command()
    async def magic8ball(self, ctx):
        """Decide your fate via this Magic 8 Ball..."""
        return await ctx.respond(random.choice([
            "Probably.", "Perhaps.", "This won't work.", "Ask Again Later!", "This answer was censored because reasons", "Yeah!", "It will do!", "Why NOT?!", "Of course!",
            "Derp", "In your dreams", "It will be done.", "Yup", "No.", "Yes.", "YES, YES YES.", "My reply is a yes.", "My Reply is a no.", "Cringe..."]))

    #Totally Random Thing
    @commands.command(hidden=True)
    async def say(self, ctx, *, sayso = None):
        """Let the bot say whatever you want."""
        autor = ctx.author
        message = ctx.message
        await message.delete()
        if sayso is not None:
            if autor.id in sparked_db.operatorlistcheck():
                async with ctx.typing():
                    saysos = await ctx.send('{0}'.format(sayso))
                    return
            else:
                return
        else:
            await ctx.send('Please Define something to say.', delete_after=10.0)
            return

    @commands.command(hidden=True)
    async def secretsay(self, ctx, channelarg, *, sayso = None):
        """Now you can make the bot talk but secretly! (Use this command in a secret channel to send a msg to a public channel)"""
        autor = ctx.author
        message = ctx.message
        await message.delete()
        if sayso is not None:
            if autor.id in sparked_db.operatorlistcheck():
                channel = await commands.TextChannelConverter().convert(ctx=ctx,argument=channelarg)
                saysos = await channel.send('{0}'.format(sayso))
                return
            else:
                return
        else:
            await ctx.send('Please Define something to say.', delete_after=10.0)
            return


    @slash_command()
    async def ping(self, ctx):
        """Pong!"""
        finallatency = self.bot.latency*10**3
        await ctx.send("Pong! ``{}ms``".format(round(finallatency, 1)))

    @commands.command(hidden=True)
    async def fixrolesasap(self, ctx):
        role = discord.utils.get(ctx.guild.roles, id=856694628194189312)

        allmembers = self.bot.get_all_members()
        i = 0
        await ctx.send("Processing...")
        for svusers in allmembers:
            if len(svusers.roles) == 1:
                await svusers.add_roles(role)
                i += 1
                print(f'Done {i} users without roles.')
        await ctx.send(f"Success! done {i} users without roles.")

def setup(bot):
    bot.add_cog(Miscellaneous(bot))
