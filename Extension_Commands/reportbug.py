#pylint: disable=unused-variable

import discord
import asyncio
import aiohttp
import emoji #Transforms Discord normal emojis (:wave:) into Discord emojis without the need of its ID's
import io #Transforms images into Bytes using (BytesIO)
from PIL import Image #Use Image from Pillow to check for image types and if they are allowed or not
from discord.ext import commands
from discord.commands import slash_command
from Databases import sparked_db

stafflist = sparked_db.operatorlistcheck()
yesemoji = '<:yes:862568274822168577>'
noemoji = '<:no:862568274901991455>'


class ReplySystem(discord.ui.View):
    def __init__(self, ctx, bot, channel, embed, embedmsg):
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
            self.embed.set_footer(text=f"User {interaction.user.name} answered:\n{bug_text.content}", icon_url=interaction.user.avatar.url)
            button.label = "Already Responded."
            button.disabled = True
            await self.embedmsg.edit(embed=self.embed, view=self)

            await interaction.followup.send(content='Bug Report responded successfully!', ephemeral=True)
            await self.context.author.send('This DM was sent successfully')
        elif interaction.user.id not in stafflist:
            return await interaction.response.send_message("You are not a staff member!", ephemeral=True)


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

    @slash_command(guild_ids=[856678143608094751])
    async def reportbug(self, ctx):
        """Creates an interactive embed where you can report bugs from Airport Simulator."""
        autor = ctx.author
        bugreportchannel = self.bot.get_channel(856678763345215508)
        embed1=discord.Embed(title="FWG Bug Report System", description="**Choose a Bug Category to proceed: **", color=0xFFFFFF)
        embed1.set_author(name=autor, icon_url=autor.avatar.url)
        embed1.set_thumbnail(url="https://cdn.discordapp.com/attachments/707431044902682644/931755527334137886/Logo4_AS_copy.png")
        embed1.add_field(name=emoji.emojize(":gear: General Bug"), value="\u200B", inline=True)
        embed1.add_field(name=emoji.emojize(":art: Model Bug"), value="\u200B", inline=True)
        embed1.add_field(name=emoji.emojize(":robot: Game-Breaking Bug"), value="\u200B", inline=True)
        embed1.add_field(name=emoji.emojize(":mag: Other"), value="\u200B", inline=True)
        embed1.add_field(name=emoji.emojize(":x: Cancel/Exit"), value="\u200B", inline=True)
        embed1.set_footer(text="This process will be automatically cancelled in 60 seconds.")
        await ctx.respond(embed=embed1)
        page1 = await ctx.interaction.original_message()
        await page1.add_reaction("⚙️")
        await page1.add_reaction("🎨")
        await page1.add_reaction("🤖")
        await page1.add_reaction("🔎")
        await page1.add_reaction(noemoji)
        def check(reaction, user):
            return user == autor and str(reaction.emoji) in ['⚙️', '🎨', '🤖', '🔎', noemoji]
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await page1.delete()
            return
        else:
            if str(reaction.emoji) == '⚙️':
                await page1.clear_reactions()
                embed2=discord.Embed(title="FWG Bug Report System", description=emoji.emojize(" :gear: General Bug Category Step 1/3"), color=0xFFFFFF)
                embed2.set_author(name=autor, icon_url=autor.avatar.url)
                embed2.set_thumbnail(url="https://cdn.discordapp.com/attachments/707431044902682644/931755527334137886/Logo4_AS_copy.png")
                embed2.add_field(name="Description:", value="These are bugs you find generally that may affect user experience.")
                embed2.set_footer(text="React with the ':yes:' emoji to continue.")
                page2 = await page1.edit(embed=embed2)
                await page1.add_reaction(yesemoji)
                await page1.add_reaction(noemoji)
                def check2(reaction, user):
                    return user == autor and str(reaction.emoji) in [yesemoji, noemoji]
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check2)
                except asyncio.TimeoutError:
                    await page1.delete()
                    await ctx.respond('The Process has been automatically cancelled! Use ``/reportbug`` again to start the command over.', ephemeral=True)
                    return
                else:
                    if str(reaction.emoji) == yesemoji:
                        await page1.clear_reactions()
                        embed3=discord.Embed(title="FWG Bug Report System", description=emoji.emojize(" :gear: General Bug Category Step 2/3"), color=0xFFFFFF)
                        embed3.set_author(name=autor, icon_url=autor.avatar.url)
                        embed3.set_thumbnail(url="https://cdn.discordapp.com/attachments/707431044902682644/931755527334137886/Logo4_AS_copy.png")
                        embed3.add_field(name="Describe the Bug!", value="Begin typing and please be specific when describing the bug")
                        embed3.set_footer(text="This process will be automatically cancelled in 120 seconds.")
                        page3 = await page1.edit(embed=embed3)
                        try:
                            bug_text = await self.bot.wait_for('message', timeout=120.0, check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id)
                        except asyncio.TimeoutError:
                            await page1.delete()
                            await ctx.respond('The Process has been automatically cancelled! Use ``/reportbug`` again to start the command over.', ephemeral=True)
                            return
                        await bug_text.delete()
                        embed4=discord.Embed(title="FWG Bug Report System", description=emoji.emojize(" :gear: General Bug Category Step 3/3"), color=0xFFFFFF)
                        embed4.set_author(name=autor, icon_url=autor.avatar.url)
                        embed4.set_thumbnail(url="https://cdn.discordapp.com/attachments/707431044902682644/931755527334137886/Logo4_AS_copy.png")
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
                        embed5.set_thumbnail(url="https://cdn.discordapp.com/attachments/707431044902682644/931755527334137886/Logo4_AS_copy.png")
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
                                finalembedgeneral.set_thumbnail(url="https://cdn.discordapp.com/attachments/707431044902682644/931755527334137886/Logo4_AS_copy.png")
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

                    elif str(reaction.emoji) == noemoji:
                        await page1.delete()
                        return await ctx.respond('The Process has been automatically cancelled! Use ``/reportbug`` again to start the command over.', ephemeral=True)

            elif str(reaction.emoji) == '🎨':
                await page1.clear_reactions()
                embed2=discord.Embed(title="FWG Bug Report System", description=emoji.emojize(" :art: Model Bug Category Step 1/3"), color=0xFFFFFF)
                embed2.set_author(name=autor, icon_url=autor.avatar.url)
                embed2.set_thumbnail(url="https://cdn.discordapp.com/attachments/707431044902682644/931755527334137886/Logo4_AS_copy.png")
                embed2.add_field(name="Description:", value="These are visual bugs that may affect user experience (incorrect colors, misplaced parts, etc.)")
                embed2.set_footer(text="React with the ':yes:' emoji to continue.")
                page2 = await page1.edit(embed=embed2)
                await page1.add_reaction(yesemoji)
                await page1.add_reaction(noemoji)
                def check2(reaction, user):
                    return user == autor and str(reaction.emoji) in [yesemoji, noemoji]
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check2)
                except asyncio.TimeoutError:
                    await page1.delete()
                    await ctx.respond('The Process has been automatically cancelled! Use ``/reportbug`` again to start the command over.', ephemeral=True)
                    return
                else:
                    if str(reaction.emoji) == yesemoji:
                        await page1.clear_reactions()
                        embed3=discord.Embed(title="FWG Bug Report System", description=emoji.emojize(" :art: Model Bug Category Step 2/3"), color=0xFFFFFF)
                        embed3.set_author(name=autor, icon_url=autor.avatar.url)
                        embed3.set_thumbnail(url="https://cdn.discordapp.com/attachments/707431044902682644/931755527334137886/Logo4_AS_copy.png")
                        embed3.add_field(name="Describe the Bug!", value="Begin typing and please be specific when describing the bug")
                        embed3.set_footer(text="This process will be automatically cancelled in 120 seconds.")
                        page3 = await page1.edit(embed=embed3)
                        try:
                            bug_text = await self.bot.wait_for('message', timeout=120.0, check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id)
                        except asyncio.TimeoutError:
                            await page1.delete()
                            await ctx.respond('The Process has been automatically cancelled! Use ``/reportbug`` again to start the command over.', ephemeral=True)
                            return
                        await bug_text.delete()
                        embed4=discord.Embed(title="FWG Bug Report System", description=emoji.emojize(" :art: Model Bug Category Step 3/3"), color=0xFFFFFF)
                        embed4.set_author(name=autor, icon_url=autor.avatar.url)
                        embed4.set_thumbnail(url="https://cdn.discordapp.com/attachments/707431044902682644/931755527334137886/Logo4_AS_copy.png")
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
                        embed5.set_thumbnail(url="https://cdn.discordapp.com/attachments/707431044902682644/931755527334137886/Logo4_AS_copy.png")
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
                                finalembedgeneral.set_thumbnail(url="https://cdn.discordapp.com/attachments/707431044902682644/931755527334137886/Logo4_AS_copy.png")
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

                    elif str(reaction.emoji) == noemoji:
                        await page1.delete()
                        return await ctx.respond('The Process has been automatically cancelled! Use ``/reportbug`` again to start the command over.', ephemeral=True)

            elif str(reaction.emoji) == '🤖':
                await page1.clear_reactions()
                embed2=discord.Embed(title="FWG Bug Report System", description=emoji.emojize(" :robot: Game-Breaking Bug Category Step 1/3"), color=0xFFFFFF)
                embed2.set_author(name=autor, icon_url=autor.avatar.url)
                embed2.set_thumbnail(url="https://cdn.discordapp.com/attachments/707431044902682644/931755527334137886/Logo4_AS_copy.png")
                embed2.add_field(name="Description:", value="These are bugs that heavily affect user experience (I lost all my data, I can't buy anything with robux, I can't earn money, etc.)")
                embed2.set_footer(text="React with the ':yes:' emoji to continue.")
                page2 = await page1.edit(embed=embed2)
                await page1.add_reaction(yesemoji)
                await page1.add_reaction(noemoji)
                def check2(reaction, user):
                    return user == autor and str(reaction.emoji) in [yesemoji, noemoji]
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check2)
                except asyncio.TimeoutError:
                    await page1.delete()
                    await ctx.respond('The Process has been automatically cancelled! Use ``/reportbug`` again to start the command over.', ephemeral=True)
                    return
                else:
                    if str(reaction.emoji) == yesemoji:
                        await page1.clear_reactions()
                        embed3=discord.Embed(title="FWG Bug Report System", description=emoji.emojize(" :robot: Game-Breaking Bug Category Step 2/3"), color=0xFFFFFF)
                        embed3.set_author(name=autor, icon_url=autor.avatar.url)
                        embed3.set_thumbnail(url="https://cdn.discordapp.com/attachments/707431044902682644/931755527334137886/Logo4_AS_copy.png")
                        embed3.add_field(name="Describe the Bug!", value="Begin typing and please be specific when describing the bug")
                        embed3.set_footer(text="This process will be automatically cancelled in 120 seconds.")
                        page3 = await page1.edit(embed=embed3)
                        try:
                            bug_text = await self.bot.wait_for('message', timeout=120.0, check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id)
                        except asyncio.TimeoutError:
                            await page1.delete()
                            await ctx.respond('The Process has been automatically cancelled! Use ``/reportbug`` again to start the command over.', ephemeral=True)
                            return
                        await bug_text.delete()
                        embed4=discord.Embed(title="FWG Bug Report System", description=emoji.emojize(" :robot: Game-Breaking Bug Category Step 3/3"), color=0xFFFFFF)
                        embed4.set_author(name=autor, icon_url=autor.avatar.url)
                        embed4.set_thumbnail(url="https://cdn.discordapp.com/attachments/707431044902682644/931755527334137886/Logo4_AS_copy.png")
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
                        embed5.set_thumbnail(url="https://cdn.discordapp.com/attachments/707431044902682644/931755527334137886/Logo4_AS_copy.png")
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
                                finalembedgeneral.set_thumbnail(url="https://cdn.discordapp.com/attachments/707431044902682644/931755527334137886/Logo4_AS_copy.png")
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

                    elif str(reaction.emoji) == noemoji:
                        await page1.delete()
                        return await ctx.respond('The Process has been automatically cancelled! Use ``/reportbug`` again to start the command over.', ephemeral=True)

            elif str(reaction.emoji) == '🔎':
                await page1.clear_reactions()
                embed2=discord.Embed(title="FWG Bug Report System", description=emoji.emojize(" :mag: Other Bug Category Step 1/3"), color=0xFFFFFF)
                embed2.set_author(name=autor, icon_url=autor.avatar.url)
                embed2.set_thumbnail(url="https://cdn.discordapp.com/attachments/707431044902682644/931755527334137886/Logo4_AS_copy.png")
                embed2.add_field(name="Description:", value="These are other bugs that aren't listed here, e.g. strange bugs that may occur.")
                embed2.set_footer(text="React with the ':yes:' emoji to continue.")
                page2 = await page1.edit(embed=embed2)
                await page1.add_reaction(yesemoji)
                await page1.add_reaction(noemoji)
                def check2(reaction, user):
                    return user == autor and str(reaction.emoji) in [yesemoji, noemoji]
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check2)
                except asyncio.TimeoutError:
                    await page1.delete()
                    await ctx.respond('The Process has been automatically cancelled! Use ``/reportbug`` again to start the command over.', ephemeral=True)
                    return
                else:
                    if str(reaction.emoji) == yesemoji:
                        await page1.clear_reactions()
                        embed3=discord.Embed(title="FWG Bug Report System", description=emoji.emojize(" :mag: Other Bug Category Step 2/3"), color=0xFFFFFF)
                        embed3.set_author(name=autor, icon_url=autor.avatar.url)
                        embed3.set_thumbnail(url="https://cdn.discordapp.com/attachments/707431044902682644/931755527334137886/Logo4_AS_copy.png")
                        embed3.add_field(name="Describe the Bug!", value="Begin typing and please be specific when describing the bug")
                        embed3.set_footer(text="This process will be automatically cancelled in 120 seconds.")
                        page3 = await page1.edit(embed=embed3)
                        try:
                            bug_text = await self.bot.wait_for('message', timeout=120.0, check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id)
                        except asyncio.TimeoutError:
                            await page1.delete()
                            await ctx.respond('The Process has been automatically cancelled! Use ``/reportbug`` again to start the command over.', ephemeral=True)
                            return
                        await bug_text.delete()
                        embed4=discord.Embed(title="FWG Bug Report System", description=emoji.emojize(" :mag: Other Bug Category Step 3/3"), color=0xFFFFFF)
                        embed4.set_author(name=autor, icon_url=autor.avatar.url)
                        embed4.set_thumbnail(url="https://cdn.discordapp.com/attachments/707431044902682644/931755527334137886/Logo4_AS_copy.png")
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
                        embed5.set_thumbnail(url="https://cdn.discordapp.com/attachments/707431044902682644/931755527334137886/Logo4_AS_copy.png")
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
                                finalembedgeneral.set_thumbnail(url="https://cdn.discordapp.com/attachments/707431044902682644/931755527334137886/Logo4_AS_copy.png")
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

                    elif str(reaction.emoji) == noemoji:
                        await page1.delete()
                        return await ctx.respond('The Process has been automatically cancelled! Use ``/reportbug`` again to start the command over.', ephemeral=True)
    
            elif str(reaction.emoji) == noemoji:
                await page1.delete()
                return await ctx.respond('The Process has been automatically cancelled! Use ``/reportbug`` again to start the command over.', ephemeral=True)

def setup(bot):
    bot.add_cog(Report(bot))