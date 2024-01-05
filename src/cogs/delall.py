import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from dateutil.relativedelta import relativedelta
import mariadb
import sys

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


bot = commands.Bot(command_prefix="&", intents=discord.Intents.all())

class delall(commands.Cog):
    def __init__ (self, bot: commands.Bot):
        self.bot = bot
        
    @app_commands.command(name="delall")
    @app_commands.default_permissions(administrator=True)
    async def delall(self, interaction: discord.Interaction):
        cur.execute("SELECT CODES FROM Codes")
        all_codes = cur.fetchall()

        cur.execute("DELETE FROM Codes", (all_codes))
        con.commit()

        await interaction.response.send_message(
            f"**{interaction.user.name}** alle Codes wurden gelöscht.",
        )
        print(f"ALLE CODES WURDEN GELÖSCHT")
        
async def setup(bot):
    await bot.add_cog(delall(bot))
    print('delall cog geladen')