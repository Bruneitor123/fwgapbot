#pylint: disable=unused-variable

import discord
import asyncio
import fwgconfig
import time
from datetime import timezone, datetime
from DMSupport.dm_support_channel import support_start


async def createFAQEmbed(faqnumber):
    if faqnumber == 1:
        message = fwgconfig.faq1
        faqtitle = fwgconfig.faqtitle1
    elif faqnumber == 2:
        message = fwgconfig.faq2
        faqtitle = fwgconfig.faqtitle2
    elif faqnumber == 3:
        message = fwgconfig.faq3
        faqtitle = fwgconfig.faqtitle3
    elif faqnumber == 4:
        message = fwgconfig.faq4
        faqtitle = fwgconfig.faqtitle4
    elif faqnumber == 5:
        message = fwgconfig.faq5
        faqtitle = fwgconfig.faqtitle5
    elif faqnumber == 6:
        message = fwgconfig.faq6
        faqtitle = fwgconfig.faqtitle6
    elif faqnumber == 7:
        message = fwgconfig.faq7
        faqtitle = fwgconfig.faqtitle7
    elif faqnumber == 8:
        message = fwgconfig.faq8
        faqtitle = fwgconfig.faqtitle8
    elif faqnumber == 9:
        message = fwgconfig.faq9
        faqtitle = fwgconfig.faqtitle9
    elif faqnumber == 10:
        message = fwgconfig.faq10
        faqtitle = fwgconfig.faqtitle10
    elif faqnumber == 11:
        message = fwgconfig.faq11
        faqtitle = fwgconfig.faqtitle11
    elif faqnumber == 12:
        message = fwgconfig.faq12
        faqtitle = fwgconfig.faqtitle12
    elif faqnumber == 13:
        message = fwgconfig.faq13
        faqtitle = fwgconfig.faqtitle13
    elif faqnumber == 14:
        message = fwgconfig.faq14
        faqtitle = fwgconfig.faqtitle14
    elif faqnumber == 15:
        message = fwgconfig.faq15
        faqtitle = fwgconfig.faqtitle15
    elif faqnumber == 16:
        message = fwgconfig.faq16
        faqtitle = fwgconfig.faqtitle16
    elif faqnumber == 17:
        message = fwgconfig.faq17
        faqtitle = fwgconfig.faqtitle17

    actualTitle = 'Automated FAQ N°: ' + str(faqnumber)
    nowtime = time.time()
    embed = discord.Embed(color=0x0040ff,title=actualTitle, url="https://fatwhalegames.com/", timestamp=datetime.fromtimestamp(nowtime, tz=timezone.utc))
    embed.add_field(name=faqtitle, value=message, inline=True)
    embed.set_footer(text=f"FAQ Entry {faqnumber}/17")
    return embed

async def createMSGEmbed(sender : discord.User, message : discord.Message):
    nowtime = time.time()
    embed = discord.Embed(color=0x0040ff,timestamp=datetime.fromtimestamp(nowtime, tz=timezone.utc))
    if len(message.attachments) > 0 and len(message.content) == 0:
        embed.set_image(url=message.attachments[0].url)
    elif len(message.attachments) > 0 and len(message.content) > 0:
        embed.add_field(name='Private Message', value=message.content, inline=True)
        embed.set_image(url=message.attachments[0].url)
    else:
        embed.add_field(name='Private Message', value=message.content, inline=True)
    
    embed.set_author(name=sender.name, icon_url=sender.avatar_url)
    embed.set_footer(text="From Fat Whale Games", icon_url='https://cdn.discordapp.com/attachments/707431044902682644/766476888234262541/FWG_BlueLogo.png')
    return embed


async def yesno_service(bot, message):
    yes_emoji = '<:yes:724011319841390592>'
    no_emoji = '<:no:724011319887396915>'
    await asyncio.sleep(2)
    problem = await message.author.send('***Was your problem solved?***')
    await problem.add_reaction(yes_emoji)
    await problem.add_reaction(no_emoji)
    def yes_no_check(reaction, user):
        return user == message.author and str(reaction.emoji) in [yes_emoji, no_emoji]
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=yes_no_check)
    except asyncio.TimeoutError:
        print('YESSS!! (Timeout)')
        return False
    else:
        if str(reaction.emoji) == yes_emoji:
            await message.author.send('Ok! Thanks for coming.', delete_after=10.0)
            await problem.delete()
            return False
        elif str(reaction.emoji) == no_emoji:
            await problem.delete()
            problemnot = await message.author.send('Do you want to start a support chat session?')
            await problemnot.add_reaction(yes_emoji)
            await problemnot.add_reaction(no_emoji)
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=yes_no_check)
            except asyncio.TimeoutError: 
                print('YESSS!! (Timeout)')
                return False
            else:
                if str(reaction.emoji) == yes_emoji:
                    await problemnot.delete()
                    return True
                elif str(reaction.emoji) == no_emoji:
                    await problemnot.delete()
                    return False

async def StartSupport(bot, message, embed):

    await message.author.send(embed=embed)
    yesno_result = await yesno_service(bot, message=message)
    if yesno_result: #If user **wants** to create a Support Channel (True)

        await support_start(bot, message)
        # ^^^^^^^^^ Will create and initiate the whole proccess of a DM Support Channel with the Bot(Staff Channel on Server)
        #and the User requesting for help(DMs)

    elif not yesno_result: #If user has **no need** of creating a Support Channel (False)
        #Do nothing
        #print('False!')
        return

async def InmediateSupport(bot, message):
    #If no FAQ was provided to the user, our bot will cordially ask to create a support session
    return await support_start(bot, message)