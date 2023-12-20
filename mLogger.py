import discord
from discord.ext import commands
from colorama import Fore
from dotenv import load_dotenv
import os
load_dotenv()
token = str(os.getenv("TOKEN"))

bot = commands.Bot(command_prefix='!' , intents= discord.Intents.all())

@bot.event
async def on_ready():
    print(f'{bot.user} is live!')
    
@bot.event            
async def on_message(message):
    print(Fore.YELLOW + f'In server: {message.guild}')
    print(Fore.GREEN + f'Message from {message.author} in channel {message.channel}: {message.content}')
            
@bot.event     
async def on_message_delete(message):
    print(Fore.YELLOW + f'In server: {message.guild}')
    print(Fore.RED + f'Message deleted from {message.author} in channel {message.channel}: {message.content}') 
@bot.event 
async def on_message_update(before, after):
    print(Fore.YELLOW + f'In server: {before.guild}')
    print(Fore.BLUE + f'**{before.author}** edited their message: \n BEFORE: {before.content} --> AFTER: {after.content}')


bot.run(token)