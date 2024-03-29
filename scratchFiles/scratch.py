import discord
from discord.ext import commands, app_commands
from datetime import datetime
from dateutil.relativedelta import relativedelta
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


class MakeBF(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="makebf", description="Make BF code. Only for Admins")
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(arg_bf="Wie soll der Code sein ? ")
    async def codeBF(self, interaction: discord.Interaction, arg_bf: str):
        await interaction.response.send_message(
            f"Ok, **{interaction.user.name}** Code für die Bestfans Rolle: `{arg_bf}`",
            ephemeral=True,
        )

        DATA_TWO = ["B", arg_bf]

        one_month_from_now = datetime.now() + relativedelta(months=1)
        DATA_TWO.append(one_month_from_now.strftime("%Y-%m-%d %H:%M:%S"))

        print(DATA_TWO)
        cur.execute(
            "INSERT INTO Codes (`USE_CASE`, CODES, `GUELTIG_BIS`) VALUES (?, ?, ?)",
            tuple(DATA_TWO),
        )
        con.commit()


async def setup(bot):
    bot.add_cog(MakeBF(bot))
    print("MakeBF cog geladen ✔️")
