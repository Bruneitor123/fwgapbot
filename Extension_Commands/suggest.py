#pylint: disable=unused-variable

import discord #Now it's Pycord
import asyncio
import emoji
from discord.ext import commands
from discord.commands import slash_command, Option
from discord.utils import find
import fwgconfig


yesemoji = '<:yes:862568274822168577>'
noemoji = '<:no:862568274901991455>'


class Suggest(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def suggest(
        self, 
        ctx, 
        suggestion: Option(str,"Type here the suggestion. It must be an In-Game feature."),
        imagelink: Option(str,"The image link in raw format to input a screenshot (https/http..)", required=False, default="")
    ):
        """Suggestion command to, well, suggest something and let developers know you really like that."""
        urlowo = await fwgconfig.serverselect(ctx)
        userboi = ctx.author
        emoji1 = yesemoji
        emoji2 = noemoji
        channel = find(lambda x:x.name == '🙂・suggestions', ctx.guild.text_channels)
        embed=discord.Embed(title=emoji.emojize("FWG Suggestions"), description=" ", color=0xFFFFFF)
        embed.set_author(name=userboi, icon_url=userboi.avatar.url)
        embed.set_thumbnail(url=urlowo)
        if len(suggestion) <= 15:
            await ctx.respond('You must have at least 15 characters to send a suggestion to avoid flooding. (We are sorry if your suggestion is really simple, please specify it!)', ephemeral=True)
            return
        elif len(suggestion) > 500:
            await ctx.respond("Sorry, you can't use more than 500 characters in a suggestion.", ephemeral=True)
            return

        if imagelink is None:
            embed.add_field(name="Suggested:", value=(f"{suggestion}"), inline=True)
        if ".png" in imagelink:
            embed.set_image(url=imagelink)
            embed.add_field(name="Suggested:", value=(f"{suggestion}"), inline=True)
        elif ".jpg" in imagelink:
            embed.set_image(url=imagelink)
            embed.add_field(name="Suggested:", value=(f"{suggestion}"), inline=True)
        elif ".jpeg" in imagelink:
            embed.set_image(url=imagelink)
            embed.add_field(name="Suggested:", value=(f"{suggestion}"), inline=True)
        elif ".gif" in imagelink:
            embed.set_image(url=imagelink)
            embed.add_field(name="Suggested:", value=(f"{suggestion}"), inline=True)
        else:
            if "https://" in imagelink:
                await ctx.respond('Unsupported file type! Remember to use an ``Image file`` format when attaching such as: ```.png - .jpg - .jpeg - .gif```', ephemeral=True)
                return
            elif "http://" in imagelink:
                await ctx.respond('Unsupported file type! Remember to use an ``Image file`` format when attaching such as: ```.png - .jpg - .jpeg - .gif```', ephemeral=True)
                return
            embed.add_field(name="Suggested:", value=(f"{imagelink} {suggestion}"), inline=True)
        await ctx.respond("Your suggestion looks nice!\nAre you sure to post this suggestion?")
        surek = await ctx.interaction.original_message()
        await surek.add_reaction(emoji1)
        await surek.add_reaction(emoji2)
        def check(reaction, user):
            return user == userboi and str(reaction.emoji) in [yesemoji, noemoji]
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await surek.delete()
            return
        else:
            await surek.delete()
            if str(reaction.emoji) == yesemoji:
                await ctx.respond('Continuing... (This may take a while)', ephemeral=True)
                async with ctx.typing():
                    #Send Embed
                    sendembed = await channel.send(embed=embed)
                    await sendembed.add_reaction(emoji1)
                    await sendembed.add_reaction(emoji2)
                    await ctx.respond(f"Your Suggestion has been posted successfully! \n[Click Here to check it out!]({sendembed.jump_url})", ephemeral=True)
                    return
            elif str(reaction.emoji) == noemoji:
                await surek.delete()
                return
 
    def num_reactions(message):
        for reaction in message.reactions:
            if str(reaction.emoji) == yesemoji:
                return reaction.count

    @slash_command()
    @discord.default_permissions(administrator=True,)
    async def suggestcount(self, ctx, 
    count: Option(int,"Number of minimum reactions to be counted."), 
    lastreactions: Option(int, "Last x messages to select from the suggestions channel.")
    ):
        """Returns amount of suggestions above specified"""
        channel = find(lambda x:x.name == '🙂・suggestions', ctx.guild.text_channels)
        async for mymessages in channel.history(limit = lastreactions):
            allReactions = mymessages.reactions
            for reaction in allReactions:
                if str(reaction.emoji) == yesemoji:
                    if reaction.count >= count:
                        await ctx.send(f'**{reaction.count} yesses reactions! Amazing upvotes!!111**\n {mymessages.jump_url}')

def setup(bot):
    bot.add_cog(Suggest(bot))