@bot.tree.command(name="make", description="Make a code. Only for Admins")
@app_commands.default_permissions(administrator=True)
async def code(
    interaction: discord.Interaction,
    arg: str,
):
    Codes = open("src/dotxml/Codes.xml", "a")
    await interaction.response.send_message(
        f"Ok, **{interaction.user.name}** der Code ist: `{arg}`", ephemeral=True
    )

    # Input von user (arg) wird in Liste DATA temporär gespeichert (bis bot neu gestartet wird).
    DATA.append("User")
    DATA.append(arg)
    DATA.append("1 Monat")
    print("Code: " + arg)

    """
    Input von user (arg) wird in .txt file ./Codes.txt gespeichert. Sodass code genutzt werden kann auch wenn der Bot neugestartet wird. 
    """

    Codes.writelines(f"User Code: {arg}\n")
    Codes.close()

    database_connect()
    print(DATA)
    print("test 1 passed")
    cur.execute("INSERT INTO codes VALUES (?, ?, ?)", DATA)
    conn.commit()

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import discord
from discord.ext import commands, tasks, app_commands
from discord import Intents
from colorama import Fore
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
import logging
import os
import sqlite3

# CONSTANTS
LOG_FILE_PATH = "src/Logs/discordPY.log"
CODES_FILE_PATH = "src/dotxml/Codes.xml"
CODE_REDEEM_LOGS_FILE_PATH = "src/dotxml/CodeRedeemLogs.xml"
ROLE_RECEIVE_LOGS_FILE_PATH = "src/dotxml/RoleReceiveLogs.xml"

load_dotenv()
token = str(os.getenv("TOKEN"))

bot = commands.Bot(command_prefix="&", intents=Intents.all())

logs_dir = "./src/Logs"
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# Logging Handler to log info
handler = logging.FileHandler(filename=LOG_FILE_PATH, encoding="utf-8", mode="w")

# Global variables
RRL = []

@bot.event
async def on_ready():
    print(f"{bot.user} is ready to rumble!")
    print("Published by Moritz Reiswaffel")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands!")
    except Exception as e:
        print(e)
    print("------------------------------")

@bot.tree.command(name="sync", app_commands.default_permissions(administrator=True))
async def sync(interaction: discord.Interaction):
    await bot.tree.sync()
    print("Command tree synced.")
    await interaction.response.send_message("Command tree synced.")

# Database connection
database_dir = "./src/Database"
if not os.path.exists(database_dir):
    os.makedirs(database_dir)

conn = sqlite3.connect(f"{database_dir}/codes.db")
cur = conn.cursor()

def database_connect():
    cur.execute("CREATE TABLE if not exists codes(Plattform, Codes, Gültig bis)"),
    cur.execute("CREATE TABLE if not exists CodeRedeemLogs(User, Code, Redeemed at)"),
    cur.execute("CREATE TABLE if not exists RoleReceiveLogs(User, Role, Received at)")

@bot.tree.command(name="makeof", description="Make OF code. Only for Admins")
@app_commands.default_permissions(administrator=True)
async def codeOF(interaction: discord.Interaction, arg_of: str):
    Codes = open(CODES_FILE_PATH, "a")
    await interaction.response.send_message(
        f"Ok, **{interaction.user.name}** Code für die Onlyfans Rolle: `{arg_of}`",
        ephemeral=True,
    )

    DATA = ["Onlyfans", arg_of]
    one_month_from_now = datetime.now() + relativedelta(months=1)
    DATA.append(one_month_from_now.strftime("%H:%M:%S %d/%m/%Y"))

    print("Onlyfans Code: " + arg_of)

    # Save code to file
    with open(CODES_FILE_PATH, "a") as Codes:
        Codes.writelines(f"Onlyfans Code: {arg_of}\n")

    # Save data to database
    database_connect()
    cur.execute("INSERT INTO codes VALUES (?, ?, ?)", DATA)
    conn.commit()
