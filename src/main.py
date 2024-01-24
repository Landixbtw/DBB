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
from dateutil.relativedelta import relativedelta

load_dotenv()
token = str(os.getenv("TOKEN"))


# logs_dir = "./Logs"
# if not os.path.exists(logs_dir):
#     print("Made Logs Folder and file!")
#     os.makedirs(logs_dir)
# # Logging Handler to log info
# handler = logging.FileHandler(
#     filename="./Logs/discord.log", encoding="utf-8", mode="w"
# )


allowed_guilds = set()  # A set to store the IDs of allowed guilds

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
        
        for file in os.listdir("./cogs"): # lists all the cog files inside the cog folder. (for raspberry /home/username/DBB/src/cogs)
            
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
        print(f'{discord.__version__}')
        print("------------------------------")
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, name=f"{bot.command_prefix}help"
            )
        )        

    async def on_guild_join(self, guild):
        # This function is called when the bot joins a new guild

        table_prefix = f"guild_{guild.id}"

        cur.execute(
            f"CREATE TABLE IF NOT EXISTS {table_prefix}_Codes (USE_CASE TEXT, CODES TEXT, GUELTIG_BIS DATETIME)"
        )
        cur.execute(
            f"CREATE TABLE IF NOT EXISTS {table_prefix}_CodeRedeemLogs (USER TEXT, CODE TEXT, REDEEMED_AT DATETIME)"
        )
        cur.execute(
            f"CREATE TABLE IF NOT EXISTS {table_prefix}_RoleReceiveLogs (USER TEXT, ROLE TEXT, USER_ID BIGINT, RECEIVED_AT DATETIME)"
        )

        con.commit()

        allowed_guilds.add(guild.id)
        
        
        for guild in bot.guilds:
            Onlyfans_Sub = discord.utils.get(guild.roles, name="Onlyfans Sub")
            Bestfans_Sub= discord.utils.get(guild.roles, name="Bestfans Sub")
            Onlyfans_Subscriber = discord.utils.get(guild.roles, name="Onlyfans Subscriber")
            Bestfans_Subscriber = discord.utils.get(guild.roles, name="Bestfans Subscriber")
            
            
            if not all((Onlyfans_Sub, Bestfans_Sub, Onlyfans_Subscriber, Bestfans_Subscriber)):
                await guild.create_role(name="Onlyfans Sub", color=0x00AFF0)
                await guild.create_role(name="Bestfans Sub", color=0xf94a25)
                
    async def on_guild_remove(self, guild):
        # This function is called when the bot is removed from a guild

        table_prefix = f"guild_{guild.id}"

        cur.execute(f"DROP TABLE IF EXISTS {table_prefix}_Codes")
        cur.execute(f"DROP TABLE IF EXISTS {table_prefix}_CodeRedeemLogs")
        cur.execute(f"DROP TABLE IF EXISTS {table_prefix}_RoleReceiveLogs")

        con.commit()
            
        for guild in bot.guilds:
            Onlyfans_Sub = discord.utils.get(guild.roles, name="Onlyfans Sub")
            Bestfans_Sub= discord.utils.get(guild.roles, name="Bestfans Sub")
        
            if all((Onlyfans_Sub, Bestfans_Sub)):
                await guild.delete_role(Onlyfans_Sub)
                await guild.delete_role(Bestfans_Sub)
    
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
        host="192.168.10.183",
        port=3306,
        database="BunnyDB",
    )
    
except mariadb.Error as mariaErr:
    print(f"Error connecting to MariaDB Platform: {mariaErr}")
    sys.exit(1)

cur = con.cursor()

@app_commands.command(name="reload", description="Reloads a Cog Class")
async def reload(interaction: discord.Interaction, cog:Literal["Cog1", "Cog2"]):
    try:
        await bot.reload_extension(name="Cogs."+cog.lower())
        await interaction.response.send_message(f"Successfully reloaded **{cog}.py**")
    except Exception as e:
        await interaction.response.send_message(f"Failed! Could not reload this cog class. See error below\n```{e}```")
    

bot = bot()

bot.help_command = MyHelp()
bot.run(token,) 