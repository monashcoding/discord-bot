from channels import *

# Import the command handler
import lightbulb
import hikari
token = "MTA1MTc3OTIwNzYxODg5NTkwMw.GmSNwu.MvzYaVh4I-gjrD3105pXdHShm1b3hQp9m9lXp0"
# Instantiate a Bot instance
bot = lightbulb.BotApp(token, prefix="!", intents=hikari.Intents.ALL, default_enabled_guilds= [810515446046523442, 804513491763200001])

# Register the command to the bot


bot.load_extensions_from('./extensions')
bot.run()
