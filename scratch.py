import discord
from discord import commands
from discord.app_commands import bot
from dotenv import load_dotenv
import os


load_dotenv()
token = str(os.getenv("TOKEN"))

bot = commands.Bot(command_prefix="!")

@bot.command()
async def ban(ctx, member: discord.Member):
    await member.ban(f"Ok, **{member.name}** has been banned.")

bot.run(token)






def liste_zu_datei(dateiname:str, liste:list) -> None:
    """
    Schreibt eine Liste in eine Datei.
    """
    with open(dateiname, "w") as f:
        f.writelines(liste)
        
def datei_zu_liste(dateiname:str) -> list:
    """
    Liest eine Datei ein und gibt eine Liste mit den Zeilen zurück.
    """
    with open(dateiname, "r") as f:
        return f.readlines()
    
    

