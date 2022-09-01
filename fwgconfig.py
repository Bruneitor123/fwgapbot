import configparser
import json
import os
import aiohttp
from dotenv import load_dotenv
from pathlib import Path

config = configparser.ConfigParser()

config.read('fwgconfig.cfg', encoding="utf8")

env_path = Path('.') / '.env'
#print(env_path)
load_dotenv(dotenv_path=env_path)
DATABASE_IP = os.getenv("DATABASE_IP")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_DATABASE = os.getenv("DATABASE_DATABASE")
DATABASE_PORT = os.getenv("DATABASE_PORT")

fwgguilds = json.loads(config.get("Settings","fwgguilds"))

async def serverselect(ctx):
    urlowo = None
    if ctx.guild.id == 856678143608094751:
        urlowo = "https://cdn.discordapp.com/attachments/707431044902682644/931755527334137886/Logo4_AS_copy.png"
    else:
        urlowo = "https://cdn.discordapp.com/attachments/707431044902682644/766476888234262541/FWG_BlueLogo.png"
    return urlowo