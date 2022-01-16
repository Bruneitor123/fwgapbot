#pylint: disable=unused-variable

import discord
import asyncio
import pymysql
import fwgconfig
import time
from datetime import timezone, datetime

DB_IP = fwgconfig.DATABASE_IP
DB_USER = fwgconfig.DATABASE_USER
DB_PASS = fwgconfig.DATABASE_PASSWORD
DB_DB = fwgconfig.DATABASE_DATABASE
DB_PORT = int(fwgconfig.DATABASE_PORT)
yes_emoji = '<:yes:724011319841390592>'

async def support_start(bot,message):
    
    db = pymysql.connect(host=DB_IP,user=DB_USER,password=DB_PASS,database=DB_DB, port=DB_PORT,charset='utf8')
    c = db.cursor()
    checkstaffavail = "SELECT `operator_id` FROM `oplist` WHERE `support_available` = '%s'"
    c.execute(checkstaffavail, True)
    wee = c.fetchall()
    oplist = [item[0] for item in wee]
    nodupelist = list(dict.fromkeys(oplist))
    if len(nodupelist) == 0:
        return await message.author.send('It seems that there is no Staff receiving support requests right now! Please try again later.', delete_after=7.0)
    lookingforstaff = await message.author.send(f'<a:loading:724344921120833647> Looking for a staff member to accept your request!\n-----> Current Staff Receiving requests: {len(nodupelist)}')



    guild = bot.get_guild(645052129710571581)
    category = discord.utils.get(guild.categories, id=720321246214094938)

    
    sql = "INSERT INTO `dmsupport` (`supportuser_id`, `supportuser_name`, `isuserticketing`) VALUES (%s, %s, %s)"
    discord_name = message.author.name+"#"+message.author.discriminator
    c.execute(sql, (message.author.id, discord_name, True))
    db.commit()

    ticketnumberis = "SELECT rowid FROM dmsupport WHERE `supportuser_id` = '%s' ORDER BY rowid DESC LIMIT 1"
    c.execute(ticketnumberis, message.author.id)
    check = c.fetchone()
    ticketNumber = int(''.join(map(str, check)))

    #Create ticket channel in open tickets category
    channel = await guild.create_text_channel(f'Ticket-{ticketNumber}', category=category)

    sql2 = "UPDATE `dmsupport` SET `channelusinguser` = %s WHERE `supportuser_id` = '%s'"
    c.execute(sql2, (channel.id, message.author.id))
    db.commit()
    async def new_ticket_embed(owner : discord.User):
        nowtime = time.time()
        embed = discord.Embed(color=0x0040ff,timestamp=datetime.fromtimestamp(nowtime, tz=timezone.utc))
        embed.add_field(name=f'Ticket created by: {owner}', value='Awaiting Staff Response!')
        discord_name = owner.name+"#"+owner.discriminator
        embed.set_author(name=discord_name, icon_url=owner.avatar_url)
        embed.set_footer(text="From Fat Whale Games", icon_url='https://cdn.discordapp.com/attachments/707431044902682644/766476888234262541/FWG_BlueLogo.png')
        return embed
    coolembed = await new_ticket_embed(owner=message.author)
    #Must ping users who are attending tickets
    emptylist = []
    for pinguser in nodupelist:
        supportuser = bot.get_user(pinguser)
        staffmentionforhelp = supportuser.mention
        emptylist.append(staffmentionforhelp)

    accepthelp = await channel.send(content=f'{emptylist} \n Awaiting Staff Approval... - ', embed=coolembed)
    
    await accepthelp.add_reaction(yes_emoji)

    def yes_no_check(reaction, user):
        return user != bot.user and str(reaction.emoji) == yes_emoji
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=3600.0,check=yes_no_check)
    except asyncio.TimeoutError:
        
        #NO USER RESPONDED TO THE TICKET, BOT WILL INMEDIATLY TRY TO CLOSE THE TICKET VIA DATABASE HANDLING

        #Update the value that checks if that channel is a ticket right now and stop listening to specific user help.
        db = pymysql.connect(host=DB_IP,user=DB_USER,password=DB_PASS,database=DB_DB, port=DB_PORT,charset='utf8')
        c = db.cursor()
        setticketuser = "UPDATE `dmsupport` SET `isuserticketing` = %s WHERE `channelusinguser` = '%s'"
        c.execute(setticketuser, (False, channel.id))

        #Get the ticket number            
        ticketnumberis = "SELECT rowid FROM dmsupport WHERE `channelusinguser` = '%s' ORDER BY rowid DESC LIMIT 1"
        c.execute(ticketnumberis, channel.id)
        check = c.fetchone()
        ticketNumber = int(''.join(map(str, check)))
        
        closedtickets = discord.utils.get(guild.channels, id=720321456223027220)
        await channel.edit(name=f'closed {ticketNumber}', category=closedtickets)
        
        await message.author.send('No one answered your ticket in 1 hour! This ticket has been auto-closed, if you need help create a ticket again, DO NOT spam this function.')
        db.close()
        return await channel.send("Channel closed succesfully!")
    else:
        print('OK!')
        await lookingforstaff.delete()
        messageboi = await channel.fetch_message(accepthelp.id)
        allReactions = messageboi.reactions
        for reaction in allReactions:
            async for oneReaction in reaction.users():
                if not oneReaction == bot.user:
                    await message.author.send(f'User {oneReaction.name} is attending your case now!')
                    hellosir = await channel.send('<a:loading:724344921120833647> Loading databases...')
                    
                    sql3 = "UPDATE `dmsupport` SET `staffuser_id` = %s WHERE `supportuser_id` = '%s'"
                    c.execute(sql3, (oneReaction.id, message.author.id))
                    db.commit()
                    await hellosir.delete()
                    await accepthelp.delete()
                    await channel.send(f'***This case is being held by: {oneReaction.name}***')
                    await channel.send('<:yes:724011319841390592> Connection established with user!')
