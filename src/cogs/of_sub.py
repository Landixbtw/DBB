import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
import mariadb
import sys

try:
    con = mariadb.connect(
        user="ole",
        password="QrsoL82",
        host="192.168.10.101",
        port=3306,
        database="BunnyDB",
    )

    # Get Cursor
    cur = con.cursor()

except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)


bot = commands.Bot(command_prefix="&", intents=discord.Intents.all())


class of_sub(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="of_sub",
        description="Enter the code you got to claim your Onlyfans role.",
    )
    
    @app_commands.describe(input="Wie lautet der Code ?")
    async def eingabe(self , interaction: discord.Interaction, input: str):
        
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
                    f"{interaction.user.name}, du hast diese Rolle schon",
                    ephemeral=True,
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


async def setup(bot):
    await bot.add_cog(of_sub(bot))
    print("of_sub cog geladen ✔️")
