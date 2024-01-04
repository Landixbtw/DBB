import discord
from discord.ext import commands
from discord import app_commands
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
import os
import mariadb
import sys
from colorama import Fore
from helpcommand import MyHelp


load_dotenv()
token = str(os.getenv("TOKEN"))

bot = commands.Bot(command_prefix="&", intents=discord.Intents.all())

logs_dir = "./src/Logs"
if not os.path.exists(logs_dir):
    print("Made Logs Folder and file!")
    os.makedirs(logs_dir)
# Logging Handler to log info
handler = logging.FileHandler(
    filename="src/Logs/discord.log", encoding="utf-8", mode="w"
)


try:
    con = mariadb.connect(
        user="ole",
        password="QrsoL82",
        host="192.168.10.183",
        port=3306,
        database="BunnyDB",
    )

    # Get Cursor
    cur = con.cursor()

except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Disable auto-commit
con.autocommit = False

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


"""
    Globale variablen für z.B. die Codes Data Liste 
    Oder Sachen die immer wieder vorkommen
"""


@bot.event
async def on_ready():
    print(f"{bot.user} is ready to rumble!")
    print("Published by Moritz Reiswaffel")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands!")
    except Exception as e:
        print(e)
    print("Everything online and working!")
    print("------------------------------")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name=f"{bot.command_prefix}help"
        )
    )


@bot.tree.command(name="sync")
@app_commands.default_permissions(administrator=True)
async def sync(interaction: discord.Interaction):
    await bot.tree.sync()
    print("Command tree synced.")
    await interaction.response.send_message("Command tree synced.")

    """
    Lässt user einen Code für of Rolle erstellen 
    Code wird in DATA und .txt file gespeichert
    
    Ephemeral in bei await.interaction.response.send_message sorgt dafür das nur der jenige der den Command ausführt die Antwort des Bots, (den Code) sehen kann.
    """


@bot.tree.command(name="makeof", description="Make OF code. Only for Admins")
@app_commands.default_permissions(administrator=True)
async def codeOF(
    interaction: discord.Interaction,
    arg_of: str,
):
    await interaction.response.send_message(
        f"Ok, **{interaction.user.name}** Code für die Onlyfans Rolle: `{arg_of}`",
        ephemeral=True,
    )

    DATA = []
    # Input von user (arg_of) wird in Liste DATA temporär gespeichert (bis bot neu gestartet wird).

    DATA.append("O")
    DATA.append(arg_of)

    one_month_from_now = datetime.now() + relativedelta(months=1)
    DATA.append(one_month_from_now.strftime("%Y-%m-%d %H:%M:%S"))

    """
    Input von user (arg_of) wird in .txt file ./Codes.xml gespeichert. Sodass code genutzt werden kann auch wenn der Bot neugestartet wird. 
    """

    print(DATA)
    cur.execute(
        "INSERT INTO Codes (`USE_CASE`, CODES, `GUELTIG_BIS`) VALUES ( ?, ?, ?)", (DATA)
    )
    con.commit()


# Gleicher Command nur für bf Rolle
@bot.tree.command(name="makebf", description="Make BF code. Only for Admins")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(arg_bf="Wie soll der Code sein ? ")
async def codeBF(interaction: discord.Interaction, arg_bf: str):
    await interaction.response.send_message(
        f"Ok, **{interaction.user.name}** Code für die Bestfans Rolle: `{arg_bf}`",
        ephemeral=True,
    )

    """
    Input von user (arg_bf) wird in .txt file src/dotxml/Codes.xml gespeichert. Sodass code genutzt werden kann auch wenn der Bot neugestartet wird. 
    """

    DATA_TWO = []
    DATA_TWO.append("B")
    DATA_TWO.append(arg_bf)

    one_month_from_now = datetime.now() + relativedelta(months=1)
    DATA_TWO.append(one_month_from_now.strftime("%Y-%m-%d %H:%M:%S"))

    print(DATA_TWO)
    cur.execute(
        "INSERT INTO Codes (`USE_CASE`, CODES, `GUELTIG_BIS`) VALUES ( ?, ?, ?)",
        (DATA_TWO),
    )
    con.commit()

    """
    code aus makeof kann hier genutzt werden um sich die Rolle zu geben. Der Input wird mit der Liste DATA abgegelichen bzw mit dem .txt file
    Darauf hin wird die Rolle gegeben oder nicht
    Ausserdem wird in einem .txt file gelogged wer und wann eine Rolle bekommen hat.
    Wenn die Person die den code einlöst die Rolle schon hat, bekommt man sie nicht nochmal, sondern der Bot antwortet "Du hast diese Rolle schon"
    """


@bot.tree.command(
    name="of_sub", description="Enter the code you got to claim your Onlyfans role."
)
@app_commands.describe(input="Wie lautet der Code ?")
async def eingabe(interaction: discord.Interaction, input: str):
    user = interaction.user

    cur.execute("SELECT CODES from Codes")
    content = cur.fetchall()
    cur.execute("SELECT USE_CASE FROM Codes")
    use_case = cur.fetchall()

    sanitized_content = [str(x[0]) for x in content]
    sanitized_use_case = [str(x[0]) for x in use_case]
    print(sanitized_content)
    print(sanitized_use_case)

    if input in sanitized_content and sanitized_use_case:
        guild = interaction.guild
        role_Onlyfans = discord.utils.get(guild.roles, name="OnlyFans Sub")
        await user.add_roles(role_Onlyfans)

        if role_Onlyfans in interaction.user.roles:
            await interaction.response.send_message(
                f"{interaction.user.name}, du hast diese Rolle schon", ephemeral=True
            )

        await interaction.response.send_message(
            f"**{interaction.user.name}** Hier ist deine Rolle.", ephemeral=True
        )

        print(f"Added role {role_Onlyfans} to {user}")

        while True:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            break

        """
        Sobald jemand einen Code einlöst wird der username, der Code und das Datum mit Uhrzeit H:M:S in die Datenbank gelogged
        """

        CRL = []
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        RRL = []
        RRL.append(user.name)
        RRL.append("O")
        RRL.append(user.id)
        RRL.append(now)
        # print(RRL)

        cur.execute("INSERT INTO RoleReceiveLogs VALUES (?, ?, ?, ?)", RRL)

        CRL.append(user.name)
        CRL.append(input)
        CRL.append(now)
        # print(CRL)

        cur.execute("INSERT INTO CodeRedeemLogs VALUES (?, ?, ?)", CRL)
        con.commit()

        async def date_handler():
            cur.execute("SELECT REDEEMED_AT FROM CodeRedeemLogs")
            date = cur.fetchone()[0]
            print(date)

            if role_Onlyfans in user.roles and date == now:
                # wenn user rolle hat und date == now entspricht rolle weg.
                user.remove_roles(role_Onlyfans)
                DM = await bot.fetch_user(interaction.user.id)
                print(f"DAS IST DIE USER ID", {DM})
                await DM.send(
                    "1 Month is over, and your Bestfans or Onlyfans role has been taken away, if you want the role again and can prove that you have a **valid subscription** of either, open a Ticket on the 'I have a question' Ticket and send a screenshot of privatebunnys respective profile so that we can see you are subscribed. "
                )

        await date_handler()

    else:
        await interaction.response.send_message(
            f"*{interaction.user.name}* du hast den falschen Code eingegeben"
        )


"""
    code aus makebf kann hier genutzt werden um sich die Rolle zu geben. Der Input wird mit der Liste DATA abgegelichen bzw mit dem .txt file
    Darauf hin wird die Rolle gegeben oder nicht
    Ausserdem wird in einem .txt file gelogged wer und wann eine Rolle bekommen hat
    """


@bot.tree.command(
    name="bf_sub", description="Enter the code you got to claim your Bestfans role."
)
@app_commands.describe(input="Wie lautet der Code ?")
async def eingabe(interaction: discord.Interaction, input: str):
    user = interaction.user

    cur.execute("SELECT CODES from Codes")
    content = cur.fetchall()
    cur.execute("SELECT USE_CASE FROM Codes")
    use_case = cur.fetchall()

    sanitized_content = [str(x[0]) for x in content]
    sanitized_use_case = [str(x[0]) for x in use_case]
    print(sanitized_content)
    print(sanitized_use_case)

    if input in sanitized_content and sanitized_use_case:
        guild = interaction.guild
        role_Bestfans = discord.utils.get(guild.roles, name="Bestfans Sub")
        await user.add_roles(role_Bestfans)

        if role_Bestfans in interaction.user.roles:
            await interaction.response.send_message(
                f"{interaction.user.name}, du hast diese Rolle schon", ephemeral=True
            )

        await interaction.response.send_message(
            f"**{interaction.user.name}** Hier ist deine Rolle.", ephemeral=True
        )

        print(f"Added role {role_Bestfans} to {user}")

        while True:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            break

        """
        Sobald jemand einen Code einlöst wird der username, der Code und das Datum mit Uhrzeit H:M:S in die Datenbank gelogged
        """

        CRL = []
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        RRL = []
        RRL.append(user.name)
        RRL.append("B")
        RRL.append(user.id)
        RRL.append(now)
        # print(RRL)

        cur.execute("INSERT INTO RoleReceiveLogs VALUES (?, ?, ?, ?)", RRL)

        CRL.append(user.name)
        CRL.append(input)
        CRL.append(now)
        # print(CRL)

        cur.execute("INSERT INTO CodeRedeemLogs VALUES (?, ?, ?)", CRL)
        con.commit()

        async def date_handler():
            cur.execute("SELECT REDEEMED_AT FROM CodeRedeemLogs")
            date = cur.fetchone()[0]
            print(date)

            if role_Bestfans in user.roles and date == now:
                # wenn user rolle hat und date == now entspricht rolle weg.
                user.remove_roles(role_Bestfans)
                DM = await bot.fetch_user(interaction.user.id)
                print(f"DAS IST DIE USER ID", {DM})
                await DM.send(
                    "1 Month is over, and your Bestfans or Onlyfans role has been taken away, if you want the role again and can prove that you have a **valid subscription** of either, open a Ticket on the 'I have a question' Ticket and send a screenshot of privatebunnys respective profile so that we can see you are subscribed. "
                )

        await date_handler()

    else:
        await interaction.response.send_message(
            f"*{interaction.user.name}* du hast den falschen Code eingegeben"
        )

        """
        Hier kann man die Codes die festegelegt wurden wieder löschen, der Bot greift auf beide .txt files zu um zu schauen ob es den Code gibt
        Und zu welcher Rolle of oder bf er gehört.
        """


@bot.tree.command(name="delete")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(input="Delete a code")
async def delete_code(interaction: discord.Interaction, input: str):
    cur.execute("SELECT CODES FROM Codes")
    all_codes = cur.fetchall()

    sanitized_list = [str(x[0]) for x in all_codes]

    if input in sanitized_list:
        cur.execute("DELETE FROM Codes WHERE CODES = ?", (input,))
        con.commit()

        updated_list = [x for x in sanitized_list if x != input]

        await interaction.response.send_message(
            f"**{interaction.user.name}** der Code `{input}` wurde gelöscht.\nFolgende Codes sind noch aktiv: {updated_list}",
            ephemeral=True,
        )
        print(f"Code {input} wurde gelöscht")

    else:
        await interaction.response.send_message(
            f"Blöd gelaufen, **{interaction.user.name}** der Code `{input}` existiert nicht"
        )

    con.close()

    """
    Dieser Command löscht alle Codes aufeinmal !
    """


@bot.tree.command(name="delall")
@app_commands.default_permissions(administrator=True)
async def delall(interaction: discord.Interaction):
    cur.execute("SELECT CODES FROM Codes")
    all_codes = cur.fetchall()

    cur.execute("DELETE FROM Codes", (all_codes))
    con.commit()

    await interaction.response.send_message(
        f"**{interaction.user.name}** alle Codes wurden gelöscht.",
    )
    print(f"ALLE CODES WURDEN GELÖSCHT")


# Zeigt alle codes an die gerade valide sind


@bot.tree.command(name="c")
@app_commands.default_permissions(administrator=True)
async def codes(interaction: discord.Interaction):
    cur.execute("SELECT CODES FROM Codes")
    all_codes = cur.fetchall()

    print(f"{interaction.user} hier sind alle Codes: \n{all_codes}")

    await interaction.response.send_message(
        f"**{interaction.user}** hier sind alle Codes: `\n{all_codes}`", ephemeral=True
    )

    if not interaction.user.has_permissions.administrator:
        interaction.response.send_message("Stop being naughty")


bot.help_command = MyHelp()

bot.run(token, log_handler=handler)
