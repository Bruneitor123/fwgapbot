import asyncio
from discord.ext import commands
from discord.commands import slash_command

playerlist = []
gameident = []
okaytoplay = True
thinkingAI = False

class TTT(commands.Cog):
    """
    Tic Tac Toe cog for FWG Discord Bot
    """

    def __init__(self, bot):
        self.bot = bot
        self.ttt_games = {}
        
    @slash_command()
    async def ttt(self, ctx):
        """ Tic Tac Toe """
        global okaytoplay
        if okaytoplay == False:
            return await ctx.respond('You can''t play, for some reason...', ephemeral=True)
        await self.ttt_new(ctx.author, ctx.channel)
        okaytoplay = False
        playerlist.append(ctx.author.id)

    async def ttt_new(self, user, channel):
        self.ttt_games[user.id] = [" "]*9
        response = self.ttt_make_board(user)
        response += "Your move:"
        msg = await channel.send(response)
        gameident.append(msg.id)
        await self.makeButtons(msg)
    
    async def ttt_move(self, user, message, move):
        # Check user currently playing
        global okaytoplay
        global thinkingAI
        uid = user.id
        if uid not in self.ttt_games:
            return await self.ttt_new(user, message.channel)
        
        # Check spot is empty
        if self.ttt_games[uid][move] == " ":
            self.ttt_games[uid][move] = "x"
        else:
            return None
        
        # Check winner
        check = self.tttDoChecks(self.ttt_games[uid])
        if check is not None:
            msgAppend = "It's a draw!" if check == "draw" else "{0} wins!".format(check[-1])
            await message.edit(content=f"{self.ttt_make_board(user)}{msgAppend}")
            await message.clear_reactions()
            okaytoplay = True
            return None
        
        # AI move
        mv = self.tttAIThink(self.tttMatrix(self.ttt_games[uid]))
        self.ttt_games[uid][self.tttCoordsToIndex(mv)] = "o"
        await message.edit(content='The AI is thinking...')
        thinkingAI = True
        await message.clear_reactions()
        await asyncio.sleep(3)
        
        # Update board
        await message.edit(content=self.ttt_make_board(user))
        thinkingAI = False
        await self.makeButtons(message)
        
        # Check winner again
        check = self.tttDoChecks(self.ttt_games[uid])
        if check is not None:
            msgAppend = "It's a draw!" if check == "draw" else "{0} wins!".format(check[-1])
            await message.edit(content=f"{self.ttt_make_board(user)}{msgAppend}")
            await message.clear_reactions()
            okaytoplay = True
    
    def ttt_make_board(self, author):
        return "{0}\n{1}\n".format(author.mention, self.tttTable(self.ttt_games[author.id]))
    
    async def makeButtons(self, msg):
        await msg.add_reaction(u"\u2196") # 0 tl
        await msg.add_reaction(u"\u2B06") # 1 t
        await msg.add_reaction(u"\u2197") # 2 tr
        await msg.add_reaction(u"\u2B05") # 3 l
        await msg.add_reaction(u"\u23FA") # 4 mid
        await msg.add_reaction(u"\u27A1") # 5 r
        await msg.add_reaction(u"\u2199") # 6 bl
        await msg.add_reaction(u"\u2B07") # 7 b
        await msg.add_reaction(u"\u2198") # 8 br


    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.message.author.id == self.bot.user.id and not user.id == self.bot.user.id:
            if user.id in playerlist and reaction.message.id in gameident:
                move = self.decodeMove(str(reaction.emoji))
                if move is not None:
                    if thinkingAI == False:
                        await self.ttt_move(user, reaction.message, move)
    
    def decodeMove(self, emoji):
        dict = {
            u"\u2196": 0,
            u"\u2B06": 1,
            u"\u2197": 2,
            u"\u2B05": 3,
            u"\u23FA": 4,
            u"\u27A1": 5,
            u"\u2199": 6,
            u"\u2B07": 7,
            u"\u2198": 8
        }
        return dict[emoji] if emoji in dict else None

    # Utility Functions
    def tttTable(self, xo):
        return (("%s%s%s\n"*3) % tuple(xo)).replace("o", ":o2:").replace("x", ":regional_indicator_x:").replace(" ", ":white_large_square:")
    
    def tttMatrix(self, b):
        return [
            [b[0], b[1], b[2]],
            [b[3], b[4], b[5]],
            [b[6], b[7], b[8]]
        ]
    def tttCoordsToIndex(self, coords):
        # it's midnight, can't think. will improve later
        map = {
            (0, 0): 0,
            (0, 1): 1,
            (0, 2): 2,
            (1, 0): 3,
            (1, 1): 4,
            (1, 2): 5,
            (2, 0): 6,
            (2, 1): 7,
            (2, 2): 8
        }
        return map[coords]
    
    def tttDoChecks(self, b):
        m = self.tttMatrix(b)
        if self.tttCheckWin(m, "x"):
            return "win X"
        if self.tttCheckWin(m, "o"):
            return "win O"
        if self.tttCheckDraw(b):
            return "draw"
        return None

    def tttFindStreaks(self, m, xo):
        row = [0, 0, 0]
        col = [0, 0, 0]
        dia = [0, 0]
        
        # Check rows and columns for X streaks
        for y in range(3):
            for x in range(3):
                if m[y][x] == xo:
                    row[y] += 1
                    col[x] += 1
        
        # Check diagonals
        if m[0][0] == xo:
            dia[0] += 1
        if m[1][1] == xo:
            dia[0] += 1
            dia[1] += 1
        if m[2][2] == xo:
            dia[0] += 1
        if m[2][0] == xo:
            dia[1] += 1
        if m[0][2] == xo:
            dia[1] += 1
            
        return (row, col, dia)
    
    def tttFindEmpty(self, matrix, rcd, n):
        # Rows
        if rcd == "r":
            for x in range(3):
                if matrix[n][x] == " ":
                    return x
        # Columns
        if rcd == "c":
            for x in range(3):
                if matrix[x][n] == " ":
                    return x
        # Diagonals
        if rcd == "d":
            if n == 0:
                for x in range(3):
                    if matrix[x][x] == " ":
                        return x
            else:
                for x in range(3):
                    if matrix[x][2-x] == " ":
                        return x
        
        return False
    
    def tttCheckWin(self, m, xo):
        row, col, dia = self.tttFindStreaks(m, xo)
        dia.append(0)
        
        for i in range(3):
            if row[i] == 3 or col[i] == 3 or dia[i] == 3:
                return True
        
        return False
    
    def tttCheckDraw(self, board):
        return not " " in board
    
    # Don't touch anything here. I forgot how it worked, it just does.
    def tttAIThink(self, m):
        rx, cx, dx = self.tttFindStreaks(m, "x")
        ro, co, do = self.tttFindStreaks(m, "o")
        
        mv = self.tttAIMove(2, m, ro, co, do)
        if mv is not False:
            return mv
        mv = self.tttAIMove(2, m, rx, cx, dx)
        if mv is not False:
            return mv
        mv = self.tttAIMove(1, m, ro, co, do)
        if mv is not False:
            return mv
        return self.tttAIMove(1, m, rx, cx, dx)
    
    def tttAIMove(self, n, m, row, col, dia):
        for r in range(3):
            if row[r] == n:
                x = self.tttFindEmpty(m, "r", r)
                if x is not False:
                    return (r, x)
            if col[r] == n:
                y = self.tttFindEmpty(m, "c", r)
                if y is not False:
                    return (y, r)
        
        if dia[0] == n:
            y = self.tttFindEmpty(m, "d", 0)
            if y is not False:
                return (y, y)
        if dia[1] == n:
            y = self.tttFindEmpty(m, "d", 1)
            if y is not False:
                return (y, 2-y)
        
        return False

def setup(bot):
    bot.add_cog(TTT(bot))