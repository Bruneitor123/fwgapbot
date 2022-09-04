#pylint: disable=unused-variable

import discord
import asyncio
import aiohttp
import emoji #Transforms Discord normal emojis (:wave:) into Discord emojis without the need of its ID's
import io #Transforms images into Bytes using (BytesIO)
from PIL import Image #Use Image from Pillow to check for image types and if they are allowed or not
from discord.ext import commands
from discord.commands import slash_command
from discord.ui import Select, View
from Databases import sparked_db
from discord.utils import find
import fwgconfig
import cryptography
stafflist = sparked_db.operatorlistcheck()
yesemoji = '<:yes:862568274822168577>'
noemoji = '<:no:862568274901991455>'


class ReplySystem(discord.ui.View):
    def __init__(self, bot, ctx, channel, embed, embedmsg):
        self.embedmsg = embedmsg
        self.embed = embed
        self.channel = channel
        self.bot = bot
        self.context = ctx
        super().__init__(timeout=None)

    @discord.ui.button(label="Mark as Fixed (Admin Only)", style=discord.ButtonStyle.green, custom_id="fwgbot:markfixed", emoji="<:yes:862568274822168577>")
    async def mark_as_fixed(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id in stafflist:
            await interaction.response.send_message("This bug has been marked as fixed!", ephemeral=True)
            self.embed.set_footer(text=f"Bug Fixed In New Servers!", icon_url="https://images.emojiterra.com/twitter/v13.1/512px/2705.png")
            button1 = [x for x in self.children if x.custom_id=="fwgbot:reply"][0]
            button1.label = "Reply disabled!"
            button1.disabled = True
            button.label = "Already marked as fixed."
            button.disabled = True
            await self.embedmsg.edit(embed=self.embed, view=self)
            await self.context.author.send('**Your bug report has been updated!**\n\nYour bug was marked as fixed in ***New Servers***!')
        elif interaction.user.id not in stafflist:
            return await interaction.response.send_message("You are not a staff member!", ephemeral=True)
        
        
    @discord.ui.button(label="Reply (Admin Only)", style=discord.ButtonStyle.blurple, custom_id="fwgbot:reply", emoji="💬")
    async def reply(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id in stafflist:
            await interaction.response.send_message("Please type in your answer to respond to this Bug Report! Timeout is 120 Seconds before this command will no longer work.", ephemeral=True)
            try:
                bug_text = await self.bot.wait_for('message', timeout=120.0, check=lambda m: m.author.id == interaction.user.id and m.channel.id == self.channel)
            except asyncio.TimeoutError:
                await interaction.followup.send('Timeout! Try to use the button again.', ephemeral=True)
                return
            
            button2 = [x for x in self.children if x.custom_id=="fwgbot:markfixed"][0]
            button2.label = "Cannot Mark as Fixed."
            button2.disabled = True
            await bug_text.delete()
            self.embed.set_footer(text=f"{interaction.user.name} answered:\n{bug_text.content}", icon_url=interaction.user.avatar.url)
            button.label = "Already Responded."
            button.disabled = True
            await self.embedmsg.edit(embed=self.embed, view=self)

            await interaction.followup.send(content='Bug Report responded successfully!', ephemeral=True)
            await self.context.author.send(f'**Your bug report has been updated!**\n\n{interaction.user.name} answered:\n{bug_text.content}')
        elif interaction.user.id not in stafflist:
            return await interaction.response.send_message("You are not a staff member!", ephemeral=True)

async def bughandlers(self, ctx, ReplySystem, bugreportchannel, option, autor):

    #Airplane Simulator server
    urlowo = await fwgconfig.serverselect(ctx)

    yesemoji = '<:yes:862568274822168577>'
    noemoji = '<:no:862568274901991455>'
    def check2(reaction, user):
        return user == autor and str(reaction.emoji) in [yesemoji, noemoji]
    if option == "General Bug":
        embed3=discord.Embed(title="FWG Bug Report System", description=emoji.emojize(" :gear: General Bug Category Step 2/3"), color=0xFFFFFF)
        embed3.set_author(name=autor, icon_url=autor.avatar.url)
        embed3.set_thumbnail(url=urlowo)
        embed3.add_field(name="Describe the Bug!", value="Begin typing and please be specific when describing the bug")
        embed3.set_footer(text="This process will be automatically cancelled in 120 seconds.")
        page1 = await ctx.respond(embed=embed3)
        try:
            bug_text = await self.bot.wait_for('message', timeout=120.0, check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id)
        except asyncio.TimeoutError:
            await page1.delete()
            await ctx.respond('The Process has been automatically cancelled! Use ``/reportbug`` again to start the command over.', ephemeral=True)
            return
        await bug_text.delete()
        embed4=discord.Embed(title="FWG Bug Report System", description=emoji.emojize(" :gear: General Bug Category Step 3/3"), color=0xFFFFFF)
        embed4.set_author(name=autor, icon_url=autor.avatar.url)
        embed4.set_thumbnail(url=urlowo)
        embed4.add_field(name="Do you have any screenshots?", value="If you have a single screenshot, send it now! If not, type '0'")
        embed4.set_footer(text="This process will be automatically cancelled in 60 seconds.")
        page4 = await page1.edit(embed=embed4)
        def check3(m):
            return m.content == '0' or len(m.attachments) > 0 and m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
        try:
            bug_image = await self.bot.wait_for('message', timeout=60.0, check=check3)
        except asyncio.TimeoutError:
            await page1.delete()
            await ctx.respond('The Process has been automatically cancelled! Use ``/reportbug`` again to start the command over.', ephemeral=True)
            return
        embed5=discord.Embed(title="FWG Bug Report System", description="Is this your final report?", color=0xFFFFFF)
        embed5.set_author(name=autor, icon_url=autor.avatar.url)
        embed5.set_thumbnail(url=urlowo)
        embed5.add_field(name="Reported a Bug:", value=bug_text.content)
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
                    await asyncio.sleep(1)
                    await page1.delete()
                    return await ctx.respond('Unsupported file type! Remember to use an ``Image file`` format when attaching. (Gifs are allowed) Use ``-reportbug`` to start the process again.', ephemeral=True)
                data.seek(0)
                secretchannel = self.bot.get_channel(725165491420921918) #Get the bug-report-images channel located in Bruno's Spaceship
                uploaded_filename_message = await secretchannel.send(f"{autor}", file=discord.File(data, filename=epicurl.filename))
                data.close()
                uploaded_filename_url = uploaded_filename_message.attachments[0].url
                embed5.set_image(url=uploaded_filename_url)
        else:
            #No Screenshots were passed / Is this your final report?
            pass
        await bug_image.delete()
        page5 = await page1.edit(embed=embed5)
        await page1.add_reaction(yesemoji)
        await page1.add_reaction(noemoji)
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check2)
        except asyncio.TimeoutError:
            await page1.delete()
            await ctx.respond('The Process has been automatically cancelled! Use ``/reportbug`` again to start the command over.', ephemeral=True)
            return
        else:
            if str(reaction.emoji) == yesemoji:
                finalembedgeneral=discord.Embed(title="FWG Bug Reports", description=emoji.emojize(f"**:gear: General Bug** by {autor.mention}"))
                finalembedgeneral.set_author(name=autor, icon_url=autor.avatar.url)
                finalembedgeneral.set_thumbnail(url=urlowo)
                finalembedgeneral.add_field(name="Reported A Bug", value=bug_text.content)
                try:
                    finalembedgeneral.set_image(url=uploaded_filename_url)
                except:
                    pass
                await page1.delete()
                finalembedlike = await bugreportchannel.send(embed=finalembedgeneral)
                view = ReplySystem(self.bot, ctx, bugreportchannel.id, embed=finalembedgeneral, embedmsg=finalembedlike)
                await finalembedlike.edit(embed=finalembedgeneral, view=view)
                return await ctx.respond(f'Your bug was reported successfully!\n [Click Here to check it out!]({finalembedlike.jump_url})', ephemeral=True)
            elif str(reaction.emoji) == noemoji:
                await page1.delete()
                return await ctx.respond('The Process has been automatically cancelled! Use ``/reportbug`` again to start the command over.', ephemeral=True)

    elif option == "Model Bug":
        embed3=discord.Embed(title="FWG Bug Report System", description=emoji.emojize(" :art: Model Bug Category Step 2/3"), color=0xFFFFFF)
        embed3.set_author(name=autor, icon_url=autor.avatar.url)
        embed3.set_thumbnail(url=urlowo)
        embed3.add_field(name="Describe the Bug!", value="Begin typing and please be specific when describing the bug")
        embed3.set_footer(text="This process will be automatically cancelled in 120 seconds.")
        page1 = await ctx.respond(embed=embed3)
        try:
            bug_text = await self.bot.wait_for('message', timeout=120.0, check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id)
        except asyncio.TimeoutError:
            await page1.delete()
            await ctx.respond('The Process has been automatically cancelled! Use ``/reportbug`` again to start the command over.', ephemeral=True)
            return
        await bug_text.delete()
        embed4=discord.Embed(title="FWG Bug Report System", description=emoji.emojize(" :art: Model Bug Category Step 3/3"), color=0xFFFFFF)
        embed4.set_author(name=autor, icon_url=autor.avatar.url)
        embed4.set_thumbnail(url=urlowo)
        embed4.add_field(name="Do you have any screenshots?", value="If you have a single screenshot, send it now! If not, type '0'")
        embed4.set_footer(text="This process will be automatically cancelled in 60 seconds.")
        page4 = await page1.edit(embed=embed4)
        def check3(m):
            return m.content == '0' or len(m.attachments) > 0 and m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
        try:
            bug_image = await self.bot.wait_for('message', timeout=60.0, check=check3)
        except asyncio.TimeoutError:
            await page1.delete()
            await ctx.respond('The Process has been automatically cancelled! Use ``/reportbug`` again to start the command over.', ephemeral=True)
            return
        embed5=discord.Embed(title="FWG Bug Report System", description=emoji.emojize("**Is this your final report?**\n**:art: Model Bug**"), color=0xFFFFFF)
        embed5.set_author(name=autor, icon_url=autor.avatar.url)
        embed5.set_thumbnail(url=urlowo)
        embed5.add_field(name="Reported a Bug:", value=bug_text.content)
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
                        #Nice! Just do nothing plz
                except:
                    await asyncio.sleep(1)
                    await page1.delete()
                    return await ctx.respond('Unsupported file type! Remember to use an ``Image file`` format when attaching. (Gifs are allowed) Use ``-reportbug`` to start the process again.', ephemeral=True)
                data.seek(0)
                secretchannel = self.bot.get_channel(725165491420921918) #Get the bug-report-images channel located in Bruno's Spaceship
                uploaded_filename_message = await secretchannel.send(f"{autor}", file=discord.File(data, filename=epicurl.filename))
                data.close()
                uploaded_filename_url = uploaded_filename_message.attachments[0].url
                embed5.set_image(url=uploaded_filename_url)
        else:
            #No Screenshots were passed / Is this your final report?
            pass
        await bug_image.delete()
        page5 = await page1.edit(embed=embed5)
        await page1.add_reaction(yesemoji)
        await page1.add_reaction(noemoji)
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check2)
        except asyncio.TimeoutError:
            await page1.delete()
            await ctx.respond('The Process has been automatically cancelled! Use ``/reportbug`` again to start the command over.', ephemeral=True)
            return
        else:
            if str(reaction.emoji) == yesemoji:
                finalembedgeneral=discord.Embed(title="FWG Bug Reports", description=emoji.emojize(f"**:art: Model Bug** by {autor.mention}"))
                finalembedgeneral.set_author(name=autor, icon_url=autor.avatar.url)
                finalembedgeneral.set_thumbnail(url=urlowo)
                finalembedgeneral.add_field(name="\u200b", value=bug_text.content)
                try:
                    finalembedgeneral.set_image(url=uploaded_filename_url)
                except:
                    pass
                await page1.delete()
                finalembedlike = await bugreportchannel.send(embed=finalembedgeneral)
                view = ReplySystem(self.bot, ctx, bugreportchannel.id, embed=finalembedgeneral, embedmsg=finalembedlike)
                await finalembedlike.edit(embed=finalembedgeneral, view=view)
                return await ctx.respond(f'Your bug was reported successfully!\n [Click Here to check it out!]({finalembedlike.jump_url})', ephemeral=True)
            elif str(reaction.emoji) == noemoji:
                await page1.delete()
                return await ctx.respond('The Process has been automatically cancelled! Use ``/reportbug`` again to start the command over.', ephemeral=True)

    elif option == "Game-Breaking Bug":
        embed3=discord.Embed(title="FWG Bug Report System", description=emoji.emojize(" :robot: Game-Breaking Bug Category Step 2/3"), color=0xFFFFFF)
        embed3.set_author(name=autor, icon_url=autor.avatar.url)
        embed3.set_thumbnail(url=urlowo)
        embed3.add_field(name="Describe the Bug!", value="Begin typing and please be specific when describing the bug")
        embed3.set_footer(text="This process will be automatically cancelled in 120 seconds.")
        page1 = await ctx.respond(embed=embed3)
        try:
            bug_text = await self.bot.wait_for('message', timeout=120.0, check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id)
        except asyncio.TimeoutError:
            await page1.delete()
            await ctx.respond('The Process has been automatically cancelled! Use ``/reportbug`` again to start the command over.', ephemeral=True)
            return
        await bug_text.delete()
        embed4=discord.Embed(title="FWG Bug Report System", description=emoji.emojize(" :robot: Game-Breaking Bug Category Step 3/3"), color=0xFFFFFF)
        embed4.set_author(name=autor, icon_url=autor.avatar.url)
        embed4.set_thumbnail(url=urlowo)
        embed4.add_field(name="Do you have any screenshots?", value="If you have a single screenshot, send it now! If not, type '0'")
        embed4.set_footer(text="This process will be automatically cancelled in 60 seconds.")
        page4 = await page1.edit(embed=embed4)
        def check3(m):
            return m.content == '0' or len(m.attachments) > 0 and m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
        try:
            bug_image = await self.bot.wait_for('message', timeout=60.0, check=check3)
        except asyncio.TimeoutError:
            await page1.delete()
            await ctx.respond('The Process has been automatically cancelled! Use ``/reportbug`` again to start the command over.', ephemeral=True)
            return
        embed5=discord.Embed(title="FWG Bug Report System", description=emoji.emojize("**Is this your final report?**\n**:robot: Game-Breaking Bug**"), color=0xFFFFFF)
        embed5.set_author(name=autor, icon_url=autor.avatar.url)
        embed5.set_thumbnail(url=urlowo)
        embed5.add_field(name="Reported a Bug:", value=bug_text.content)
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
                        #Nice! Just do nothing plz
                except:
                    await asyncio.sleep(1)
                    await page1.delete()
                    return await ctx.respond('Unsupported file type! Remember to use an ``Image file`` format when attaching. (Gifs are allowed) Use ``-reportbug`` to start the process again.', ephemeral=True)
                data.seek(0)
                secretchannel = self.bot.get_channel(725165491420921918) #Get the bug-report-images channel located in Bruno's Spaceship
                uploaded_filename_message = await secretchannel.send(f"{autor}", file=discord.File(data, filename=epicurl.filename))
                data.close()
                uploaded_filename_url = uploaded_filename_message.attachments[0].url
                embed5.set_image(url=uploaded_filename_url)
        else:
            #No Screenshots were passed / Is this your final report?
            pass
        await bug_image.delete()
        page5 = await page1.edit(embed=embed5)
        await page1.add_reaction(yesemoji)
        await page1.add_reaction(noemoji)
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check2)
        except asyncio.TimeoutError:
            await page1.delete()
            await ctx.respond('The Process has been automatically cancelled! Use ``/reportbug`` again to start the command over.', ephemeral=True)
            return
        else:
            if str(reaction.emoji) == yesemoji:
                finalembedgeneral=discord.Embed(title="FWG Bug Reports", description=emoji.emojize(f"**:robot: Game-Breaking Bug** by {autor.mention}"))
                finalembedgeneral.set_author(name=autor, icon_url=autor.avatar.url)
                finalembedgeneral.set_thumbnail(url=urlowo)
                finalembedgeneral.add_field(name="\u200b", value=bug_text.content)
                try:
                    finalembedgeneral.set_image(url=uploaded_filename_url)
                except:
                    pass
                await page1.delete()
                finalembedlike = await bugreportchannel.send(embed=finalembedgeneral)
                view = ReplySystem(self.bot, ctx, bugreportchannel.id, embed=finalembedgeneral, embedmsg=finalembedlike)
                await finalembedlike.edit(embed=finalembedgeneral, view=view)
                return await ctx.respond(f'Your bug was reported successfully!\n [Click Here to check it out!]({finalembedlike.jump_url})', ephemeral=True)
            elif str(reaction.emoji) == noemoji:
                await page1.delete()
                return await ctx.respond('The Process has been automatically cancelled! Use ``/reportbug`` again to start the command over.', ephemeral=True)

    elif option == "Other":
        embed3=discord.Embed(title="FWG Bug Report System", description=emoji.emojize(" :mag: Other Bug Category Step 2/3"), color=0xFFFFFF)
        embed3.set_author(name=autor, icon_url=autor.avatar.url)
        embed3.set_thumbnail(url=urlowo)
        embed3.add_field(name="Describe the Bug!", value="Begin typing and please be specific when describing the bug")
        embed3.set_footer(text="This process will be automatically cancelled in 120 seconds.")
        page1 = await ctx.respond(embed=embed3)
        try:
            bug_text = await self.bot.wait_for('message', timeout=120.0, check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id)
        except asyncio.TimeoutError:
            await page1.delete()
            await ctx.respond('The Process has been automatically cancelled! Use ``/reportbug`` again to start the command over.', ephemeral=True)
            return
        await bug_text.delete()
        embed4=discord.Embed(title="FWG Bug Report System", description=emoji.emojize(" :mag: Other Bug Category Step 3/3"), color=0xFFFFFF)
        embed4.set_author(name=autor, icon_url=autor.avatar.url)
        embed4.set_thumbnail(url=urlowo)
        embed4.add_field(name="Do you have any screenshots?", value="If you have a single screenshot, send it now! If not, type '0'")
        embed4.set_footer(text="This process will be automatically cancelled in 60 seconds.")
        page4 = await page1.edit(embed=embed4)
        def check3(m):
            return m.content == '0' or len(m.attachments) > 0 and m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
        try:
            bug_image = await self.bot.wait_for('message', timeout=60.0, check=check3)
        except asyncio.TimeoutError:
            await page1.delete()
            await ctx.respond('The Process has been automatically cancelled! Use ``/reportbug`` again to start the command over.', ephemeral=True)
            return
        embed5=discord.Embed(title="FWG Bug Report System", description=emoji.emojize("**Is this your final report?**\n**:mag: Other Bug**"), color=0xFFFFFF)
        embed5.set_author(name=autor, icon_url=autor.avatar.url)
        embed5.set_thumbnail(url=urlowo)
        embed5.add_field(name="Reported a Bug:", value=bug_text.content)
        if len(bug_image.attachments) > 0:
            async with ctx.typing():
                epicurl = bug_image.attachments[0]
                #Do the thing Daniel told me to - send the image to another server and boom epic
                async with aiohttp.ClientSession() as session:
                        async with session.get(epicurl.url) as resp:
                            if resp.status != 200:
                                return await ctx.respond('Could not download file...')
                            data = io.BytesIO(await resp.read())
                try:
                    with Image.open(data) as image_pil:
                        pass
                        #Nice! Just do nothing plz
                except:
                    await asyncio.sleep(1)
                    await page1.delete()
                    return await ctx.respond('Unsupported file type! Remember to use an ``Image file`` format when attaching. (Gifs are allowed) Use ``-reportbug`` to start the process again.', ephemeral=True)
                data.seek(0)
                secretchannel = self.bot.get_channel(725165491420921918) #Get the bug-report-images channel located in Bruno's Spaceship
                uploaded_filename_message = await secretchannel.send(f"{autor}", file=discord.File(data, filename=epicurl.filename))
                data.close()
                uploaded_filename_url = uploaded_filename_message.attachments[0].url
                embed5.set_image(url=uploaded_filename_url)
        else:
            #No Screenshots were passed / Is this your final report?
            pass
        await bug_image.delete()
        page5 = await page1.edit(embed=embed5)
        await page1.add_reaction(yesemoji)
        await page1.add_reaction(noemoji)
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check2)
        except asyncio.TimeoutError:
            await page1.delete()
            await ctx.respond('The Process has been automatically cancelled! Use ``/reportbug`` again to start the command over.', ephemeral=True)
            return
        else:
            if str(reaction.emoji) == yesemoji:
                finalembedgeneral=discord.Embed(title="FWG Bug Reports", description=emoji.emojize(f"**:mag: Other Bug** by {autor.mention}"))
                finalembedgeneral.set_author(name=autor, icon_url=autor.avatar.url)
                finalembedgeneral.set_thumbnail(url=urlowo)
                finalembedgeneral.add_field(name="\u200b", value=bug_text.content, inline=False)
                try:
                    finalembedgeneral.set_image(url=uploaded_filename_url)
                except:
                    pass
                await page1.delete()
                finalembedlike = await bugreportchannel.send(embed=finalembedgeneral)
                view = ReplySystem(self.bot, ctx, bugreportchannel.id, embed=finalembedgeneral, embedmsg=finalembedlike)
                #Store to database for persistent view
                #sparked_db.inserttoreportbug(self.bot, autor, bugreportchannel, finalembedgeneral, finalembedlike)
                await finalembedlike.edit(embed=finalembedgeneral, view=view)
                return await ctx.respond(f'Your bug was reported successfully!\n [Click Here to check it out!]({finalembedlike.jump_url})', ephemeral=True)
            elif str(reaction.emoji) == noemoji:
                await page1.delete()
                return await ctx.respond('The Process has been automatically cancelled! Use ``/reportbug`` again to start the command over.', ephemeral=True)

    elif option == "Cancel/Exit":
        return await ctx.respond('The Process has been automatically cancelled! Use ``/reportbug`` again to start the command over.', ephemeral=True)
    pass

class Report(commands.Cog):
    
    def __init__(self, bot):
        #super().__init__()
        #self.persistent_views_added = False
        self.bot = bot

    # @commands.Cog.listener("on_ready")
    # async def when_readyplz(self):
    #     if not self.persistent_views_added:
    #         for bot, user, channel, embed, embedmsg in sparked_db.checkreportbug2():
    #             commands.Bot.add_view(ReplySystem(bot, user, channel, embed, embedmsg))
    #         self.persistent_views_added = True

    @slash_command()
    async def reportbug(self, ctx):
        """Creates an interactive embed where you can report bugs from Airport Simulator."""
        select2 = Select(placeholder="Select the game you are referring the report to", options=[
        discord.SelectOption(label="Airport Tycoon", description="Main FWG Game.", emoji="<:fwg:769681026469068810>"),
        discord.SelectOption(label="Plane Simulator", description="This is Plane Simulator Game", emoji="<:plane:949433161081843762>"),
        discord.SelectOption(label="Splatter Blocks", description="And this is Splatter Blocks Game", emoji="🎨"),
        discord.SelectOption(label="Cancel/Exit", description="", emoji=f"{noemoji}")])


        select = Select(placeholder="Select a Bug Category", options=[
        discord.SelectOption(label="General Bug", description="Bugs that may affect user experience.", emoji="⚙️"),
        discord.SelectOption(label="Model Bug", description="Visual errors (incorrect colors, misplaced parts, etc.)", emoji="🎨"),
        discord.SelectOption(label="Game-Breaking Bug", description="Bugs that break your game (I lost all my data, etc.)", emoji="🤖"),
        discord.SelectOption(label="Other Bugs", description="Other bugs that aren't listed here, e.g. strange errors.", emoji="🔎"),
        discord.SelectOption(label="Cancel/Exit", description="", emoji=f"{noemoji}")])
        
        autor = ctx.author
        embed1=discord.Embed(title="FWG Bug Report System", description="**Choose a Bug Category to proceed: **", color=0xFFFFFF)
        embed1.set_author(name=autor, icon_url=autor.avatar.url)
        async def interaction_check(interaction) -> bool:
            if interaction.user.id != autor.id:
                await interaction.response.send_message('You are not the owner of this interaction!', ephemeral=True)
                return False
            else:
                return True

        async def the_callback(interaction):
            global papu
            option2 = select.values[0]
            bugreportchannel = papu
            if option2 == "General Bug":
                await bughandlers(self, ctx, ReplySystem, bugreportchannel, option2, autor)
            elif option2 == "Model Bug":
                await bughandlers(self, ctx, ReplySystem, bugreportchannel, option2, autor)
            elif option2 == "Game-Breaking Bug":
                await bughandlers(self, ctx, ReplySystem, bugreportchannel, option2, autor)
            elif option2 == "Other":
                await bughandlers(self, ctx, ReplySystem, bugreportchannel, option2, autor)
            elif option2 == "Cancel/Exit":
                return await interaction.response.send_message('The Process has been cancelled! Use ``/reportbug`` again to start the command over.', ephemeral=True)

        async def new_callback(interaction):
            global papu
            page1 = await ctx.interaction.original_message()
            await page1.delete()
            option = select2.values[0]
            if option == "Airport Tycoon":
                bugreportchannel = self.bot.get_channel(681730197275541504) # Airport Tycoon ID for Bug Report Channel
                
                papu = bugreportchannel
                embed1.set_footer(text=f"Bug-Report Channel Detected: {bugreportchannel.name}")
                select.callback = the_callback
                thaview = View()
                thaview.author = ctx.author.id
                thaview.interaction_check = interaction_check
                thaview.add_item(select)
                return await ctx.respond(embed=embed1, view=thaview, ephemeral=True)


            elif option == "Plane Simulator":
                bugreportchannel = self.bot.get_channel(856678763345215508) # Plane Sim ID CH
                papu = bugreportchannel
                embed1.set_footer(text=f"Bug-Report Channel Detected: {bugreportchannel.name}")
                select.callback = the_callback
                thaview = View()
                thaview.author = ctx.author.id
                thaview.interaction_check = interaction_check
                thaview.add_item(select)
                return await ctx.respond(embed=embed1, view=thaview, ephemeral=True)


            elif option == "Splatter Blocks":
                bugreportchannel = self.bot.get_channel(1015025282006138961) # SB ID CH
                papu = bugreportchannel
                embed1.set_footer(text=f"Bug-Report Channel Detected: {bugreportchannel.name}")
                select.callback = the_callback
                thaview = View()
                thaview.author = ctx.author.id
                thaview.interaction_check = interaction_check
                thaview.add_item(select)
                return await ctx.respond(embed=embed1, view=thaview, ephemeral=True)


            elif option == "Cancel/Exit":
                return await interaction.response.send_message('The Process has been cancelled! Use ``/reportbug`` again to start the command over.', ephemeral=True)

        select2.callback = new_callback
        firstview = View()
        firstview.author = ctx.author.id
        firstview.interaction_check = interaction_check
        firstview.add_item(select2)
        await ctx.respond(embed=embed1, view=firstview)
        


        


def setup(bot):
    bot.add_cog(Report(bot))