import nextcord
from nextcord.ext import commands

intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix='.', intents=intents)
extensions = [
    "responses",
    "database"
]

if __name__ == "__main__":
    for ext in extensions:
        bot.load_extension(ext)


@bot.event
async def on_ready():
    print("Bot is ready!")

token = "MTE1MjgyMDUzNjY0NTI1NTIxOA.Gj1TWM.kqf-2kGD53FGk7cAeJ18pEOLehwl5PnLBtf3bs"
bot.run(token)
