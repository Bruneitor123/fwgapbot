import configparser

config = configparser.ConfigParser()

config.read('Giveaway_Setup/config.ini')

modrole = config['SETTINGS']['modrole'].strip()
riggers = config['SETTINGS']['riggers'].split(",")
dmAllowed = config['SETTINGS']['dmAllowed'].split(",")

try:
	riggers.remove("")
except:
	pass
	
try:
	dmAllowed.remove("")
except:
	pass