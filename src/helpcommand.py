import discord
from discord.ext import commands
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='&', intents=intents)

# https://gist.github.com/InterStella0/b78488fb28cadf279dfd3164b9f0cf96

class MyHelp(commands.HelpCommand):
    #&help
    async def send_bot_help(self, mapping):
        await self.context.send('*These two commands are important for you*:\n1. /of_sub: enter the code you got to receive your role.\n2. /bf_sub: enter the code you got to receive your role.')
        
