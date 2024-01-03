import discord
from discord.ext import commands
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='&', intents=intents)

class MyHelp(commands.HelpCommand):
    #&help
    async def send_bot_help(self, mapping):
        await self.context.send('*These two commands are important for you*:\n1. /of_sub: enter the code you got from privatebunny to receive your role.\n2. /bf_sub: enter the code you got from privatebunny to receive your role.')
        
    #&help<command>
    async def send_command_help(self, command):
        await self.context.send('Das ist ein Hilfe command')
        
    #&help<group>
    async def send_group_help(self, group): 
        await self.context.send('Das ist eine Hilfe gruppe')
    
    #&help<cog>
    async def send_cog_help(self, cog): 
        await self.context.send('Das ist ein help cog')
    
    
