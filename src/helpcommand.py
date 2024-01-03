import discord
from discord.ext import commands
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='&', intents=intents)

class MyHelp(commands.HelpCommand):
    #&help
    async def send_bot_help(self, mapping):
        await self.context.send('Das ist der Hilfe command')
        
    #&help<command>
    async def send_command_help(self, command):
        await self.context.send('Das ist ein Hilfe command')
        
    #&help<group>
    async def send_group_help(self, group): 
        await self.context.send('Das ist eine Hilfe gruppe')
    
    #&help<cog>
    async def send_cog_help(self, cog): 
        await self.context.send('Das ist ein help cog')
    
    
