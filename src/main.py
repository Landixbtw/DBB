import discord
from discord.ext import commands
from discord import app_commands
import logging
from dotenv import load_dotenv
import os
import mariadb
import sys
from colorama import Fore
from helpcommand import MyHelp
from typing import Literal


load_dotenv()
token = str(os.getenv("TOKEN"))


logs_dir = "./src/Logs"
if not os.path.exists(logs_dir):
    print("Made Logs Folder and file!")
    os.makedirs(logs_dir)
# Logging Handler to log info
handler = logging.FileHandler(
    filename="./src/Logs/discord.log", encoding="utf-8", mode="w"
)

class bot(commands.Bot):
    def __init__(self, ):
        super().__init__(
            command_prefix="&", intents=discord.Intents.all()
        )
        
        self.cogList: list[str] = [
            "makeof",
            "bf_sub",
            "c",
            "delall",
            "delete",
            "makebf",
            "of_sub",
            
        ]
    
    async def setup_hook(self): 
        print('loading cogs ...') 
        
        for file in os.listdir("./src/cogs"): # lists all the cog files inside the cog folder. (for raspberry /home/username/DBB/src/cogs)
            
            if file.endswith(".py"): # It gets all the cogs that ends with a ".py".
                try:
                    name = file[:-3] # It gets the name of the file removing the ".py"
                    await bot.load_extension(f"cogs.{name}") # This loads the cog.
                except Exception as e:
                    print(f'error: {e}') 
                    
    async def on_ready(self):
        print(f"{bot.user.name} is ready to rumble!")
        print("Published by Moritz Reiswaffel")
        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} commands!")
        except Exception as e:
            print(e)
        #print(f'{discord.__version__}')
        print("------------------------------")
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, name=f"{bot.command_prefix}help"
            )
        )


                    
async def reload_hook(self):
        print('reloading cogs')
        for file in os.listdir("./src/cogs"):
            if file.endswith('.py'):
                try:
                    name = file[:-3]
                    await bot.reload_extension(f'cogs.{name}')
                except Exception as reErr:
                    print(f'Reload error: {reErr}')
                        


try:
    con = mariadb.connect(
        user="ole",
        password="QrsoL82",
        host="192.168.10.101",
        port=3306,
        database="BunnyDB",
    )
    
except mariadb.Error as mariaErr:
    print(f"Error connecting to MariaDB Platform: {mariaErr}")
    sys.exit(1)



# # con.autocommit = False

cur = con.cursor()

cur.execute(
    "CREATE TABLE IF NOT EXISTS Codes(USE_CASE TEXT, CODES TEXT , GUELTIG_BIS DATETIME)"
)
cur.execute(
    "CREATE TABLE IF NOT EXISTS CodeRedeemLogs(USER TEXT, CODE TEXT, REDEEMED_AT DATETIME)"
)
cur.execute(
    "CREATE TABLE IF NOT EXISTS RoleReceiveLogs(USER TEXT, ROLE TEXT, USER_ID BIGINT , RECEIVED_AT DATETIME)"
)

con.commit()


@app_commands.command(name="reload", description="Reloads a Cog Class")
async def reload(interaction: discord.Interaction, cog:Literal["Cog1", "Cog2"]):
    try:
        await bot.reload_extension(name="Cogs."+cog.lower())
        await interaction.response.send_message(f"Successfully reloaded **{cog}.py**")
    except Exception as e:
        await interaction.response.send_message(f"Failed! Could not reload this cog class. See error below\n```{e}```")
    

bot = bot()
bot.help_command = MyHelp()
bot.run(token, log_handler=handler, reconnect=True) 
