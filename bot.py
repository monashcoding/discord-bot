from channels import *

# Import the command handler
import lightbulb
import hikari
token = "MTA1MTc3OTIwNzYxODg5NTkwMw.GobsLT.5Gd7ImBp8ZdzUQNRszE4GN4Glf8GVVw6Eus6Nw"
# Instantiate a Bot instance
bot = lightbulb.BotApp(token, prefix="!", intents=hikari.Intents.ALL, default_enabled_guilds= [810515446046523442, 804513491763200001])

# Register the command to the bot


bot.load_extensions_from('./extensions')
bot.run()
