# loading super secret bot tokens...
from dotenv import load_dotenv
load_dotenv()
import os
# Environ variables
token = os.getenv('token')
# Import the command handler
import lightbulb
import hikari
# Instantiate a Bot instance
bot = lightbulb.BotApp(token, prefix="!", intents=hikari.Intents.ALL, default_enabled_guilds= [810515446046523442, 80451349176320000]) 

# Register the command to the bot


bot.load_extensions_from('./extensions')
bot.run()
