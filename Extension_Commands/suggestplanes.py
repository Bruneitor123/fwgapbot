#pylint: disable=unused-variable

import discord
import aiohttp
import asyncio
import emoji
import io
import cryptography
from PIL import Image
from discord.ext import commands
from discord.commands import slash_command
from discord.utils import find
from Databases import sparked_db


yesemoji = '<:yes:862568274822168577>'
noemoji = '<:no:862568274901991455>'

class SuggestPlanes(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    @slash_command()
    async def planesuggest(
        self, 
        ctx
        ):
        """Suggest your favorite plane! """
        autor = ctx.author
        planechannel = find(lambda x:x.name == '🛩・plane-suggestions', ctx.guild.text_channels)
        if planechannel is None:
            return await ctx.respond('There was no plane suggestions channel found. (This command is Only available for [Airplane Simulator](https://discord.gg/xD3x4pVDV6))', ephemeral=True)
            
        embed1=discord.Embed(title="FWG Plane Suggestion System", description="**You are about to create a plane suggestion, do you want to proceed?**", color=0xFFFFFF)
        embed1.set_author(name=autor, icon_url=autor.avatar.url)
        embed1.set_thumbnail(url="https://cdn.discordapp.com/attachments/707431044902682644/931755527334137886/Logo4_AS_copy.png")
        embed1.set_footer(text="This process will be automatically cancelled in 60 seconds.")
        await ctx.respond(embed=embed1)
        page1 = await ctx.interaction.original_response()
        await page1.add_reaction(yesemoji)
        await page1.add_reaction(noemoji)
        def check(reaction, user):
            return user == autor and str(reaction.emoji) in [yesemoji, noemoji]

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await page1.delete()
            await ctx.respond('Process Automatically Cancelled, use ``/planesuggest`` to start the command over.', ephemeral=True)
            return
        else:
            if str(reaction.emoji) == yesemoji:
                await page1.clear_reactions()

                if sparked_db.toomanyplanes(autor):
                    await page1.delete()
                    return await ctx.respond(f"You have already made your 3 monthly plane suggestions! Please wait until: {sparked_db.planecooldown(autor)}", ephemeral=True)
                
                embed3=discord.Embed(title="FWG Plane Suggestion System", description=emoji.emojize(" Step 2/4 - Name your Plane!"), color=0xFFFFFF)
                embed3.set_author(name=autor, icon_url=autor.avatar.url)
                embed3.set_thumbnail(url="https://cdn.discordapp.com/attachments/707431044902682644/931755527334137886/Logo4_AS_copy.png")
                embed3.add_field(name="Name your Plane!", value="Begin typing and please be specific when writing your plane, always try to put the Manufacturer and the Model name like: ***Boeing 777X***")
                embed3.set_footer(text="This process will be automatically cancelled in 120 seconds.")
                page3 = await page1.edit(embed=embed3)
                try:
                    bug_text = await self.bot.wait_for('message', timeout=120.0, check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id)
                except asyncio.TimeoutError:
                    await page1.delete()
                    await ctx.respond('Process Cancelled, use ``/planesuggest`` to start the command over.', ephemeral=True)
                    return
                await bug_text.delete()
                if len(bug_text.content) >= 30:
                    return await ctx.respond('You can''t suggest a plane with more than 30 characters.', ephemeral=True)

                tempplaneslist, msglinklist = sparked_db.dbchecklistap(bug_text=bug_text.content)

                if bug_text.content in tempplaneslist:
                    await page1.delete()
                    myembed=discord.Embed(title=emoji.emojize("Your plane has already been suggested! :tools:"), description=f"[Go to the Suggested Plane Link!]({msglinklist[0]})", color=0xFF0000)
                    myembed.set_author(name=autor, icon_url=autor.avatar.url)
                    myembed.set_thumbnail(url="https://www.freeiconspng.com/uploads/error-icon-15.png")
                    myembed.add_field(name="Your plane has been already suggested!", value=" Use ``/planesuggest`` to start the command over.", inline=False)
                    return await ctx.respond(embed=myembed, ephemeral=True)

                embed4=discord.Embed(title="FWG Plane Suggestion System", description=emoji.emojize(" Step 3/4 - Put a Plane Image!"), color=0xFFFFFF)
                embed4.set_author(name=autor, icon_url=autor.avatar.url)
                embed4.set_thumbnail(url="https://cdn.discordapp.com/attachments/707431044902682644/931755527334137886/Logo4_AS_copy.png")
                embed4.add_field(name="Post a mandatory Plane Image/Gif", value="If you have a **single** screenshot, send it now so users will be able to see your epic plane! If not, redo the command when you have one.")
                embed4.set_footer(text="This process will be automatically cancelled in 60 seconds.")
                page4 = await page1.edit(embed=embed4)
                def check3(m):
                    return len(m.attachments) > 0 and m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
                try:
                    bug_image = await self.bot.wait_for('message', timeout=60.0, check=check3)
                except asyncio.TimeoutError:
                    await page1.delete()
                    await ctx.respond('Process Cancelled, use ``/planesuggest`` to start the command over.', ephemeral=True)
                    return
                embed5=discord.Embed(title="FWG Plane Suggestion System", description="Step 4/4 - Review your Plane!", color=0xFFFFFF)
                embed5.set_author(name=autor, icon_url=autor.avatar.url)
                embed5.set_thumbnail(url="https://cdn.discordapp.com/attachments/707431044902682644/931755527334137886/Logo4_AS_copy.png")
                embed5.add_field(name="Suggested a new plane:", value=bug_text.content)
                if len(bug_image.attachments) > 0:
                    async with ctx.typing():
                        epicurl = bug_image.attachments[0]
                        #Do the thing Daniel told me to - send the image to another server and boom epic
                        async with aiohttp.ClientSession() as session:
                                async with session.get(epicurl.url) as resp:
                                    if resp.status != 200:
                                        return await ctx.respond('Could not download file... (Is Discord working correctly?)', ephemeral=True)
                                    data = io.BytesIO(await resp.read())
                        try:
                            with Image.open(data) as image_pil:
                                pass
                                #Nice!
                        except:
                            await page1.delete()
                            return await ctx.respond('Unsupported file type! Remember to use an ``Image file`` format when attaching. (Gifs are allowed) Use ``/planesuggest`` to start the process again.', ephemeral=True)
                        data.seek(0)
                        secretchannel = self.bot.get_channel(930982213879734292) #Get the bug-report-images channel located in Bruno's Spaceship
                        uploaded_filename_message = await secretchannel.send(f"{autor}", file=discord.File(data, filename=epicurl.filename))
                        data.close()
                        uploaded_filename_url = uploaded_filename_message.attachments[0].url
                        await asyncio.sleep(2.4)
                        embed5.set_image(url=uploaded_filename_url)
                else:
                    return await ctx.respond(emoji.emojize(':x: You must attach one image/screenshot to Suggest a Plane.'), ephemeral=True)
                await bug_image.delete()
                page5 = await page1.edit(embed=embed5)
                await page1.add_reaction(yesemoji)
                await page1.add_reaction(noemoji)
                def check2(reaction, user):
                    return user == autor and str(reaction.emoji) in [yesemoji, noemoji]
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check2)
                except asyncio.TimeoutError:
                    await page1.delete()
                    await ctx.respond('Process Cancelled, use ``/planesuggest`` to start the command over.', ephemeral=True)
                    return
                else:
                    if str(reaction.emoji) == yesemoji:
                        finalembedgeneral=discord.Embed(title="FWG Plane Suggestions", description=f"**Plane Name**: {bug_text.content}")
                        finalembedgeneral.set_author(name=autor, icon_url=autor.avatar.url)
                        finalembedgeneral.set_thumbnail(url="https://cdn.discordapp.com/attachments/707431044902682644/931755527334137886/Logo4_AS_copy.png")
                        try:
                            finalembedgeneral.set_image(url=uploaded_filename_url)
                        except:
                            pass
                        await page1.delete()
                        theepic = await planechannel.send(embed=finalembedgeneral)
                        await theepic.add_reaction(yesemoji)
                        await theepic.add_reaction(noemoji)
                        #Force connection to the DB since I'm to lazy to code a section for 4 values in an MySQL INSERT Function xD
                        db, c = sparked_db.connectplz()

                        insertuser = "INSERT INTO `airplanelist` (`suggester_id`,`suggester_name`,`airplane_name`,`message_link`) VALUES (%s, %s, %s,%s)"
                        c.execute(insertuser, (autor.id, autor.name, bug_text.content, theepic.jump_url))
                        db.commit()
                        db.close()

                        return await ctx.respond('Your plane was posted successfully!', ephemeral=True)
                    elif str(reaction.emoji) == noemoji:
                        await page1.delete()
                        return await ctx.respond('Process Cancelled, use ``/planesuggest`` to start the command over.', ephemeral=True)

            elif str(reaction.emoji) == noemoji:
                await page1.delete()
                return await ctx.respond('Process Cancelled, use ``/planesuggest`` to start the command over.', ephemeral=True)

def setup(bot):
    bot.add_cog(SuggestPlanes(bot))