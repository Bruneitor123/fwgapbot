import configparser
import json
import os
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


pingbotrandomanswers = json.loads(config.get("Settings","pingbotrandomanswers"))