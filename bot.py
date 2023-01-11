from channels import *

# Import the command handler
import lightbulb
import hikari
token = "MTA1MTc3OTIwNzYxODg5NTkwMw.GxDLFz.gyK0XRA49XLbhqL4-3SJHAYtiLiy8m5VLRZJOA"
# Instantiate a Bot instance
bot = lightbulb.BotApp(token, prefix="!", intents=hikari.Intents.ALL, default_enabled_guilds= [810515446046523442, 804513491763200001])

# Register the command to the bot


bot.load_extensions_from('./extensions')
bot.run()
