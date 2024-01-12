import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from dateutil.relativedelta import relativedelta
import mariadb
import sys


bot = commands.Bot(command_prefix="&", intents=discord.Intents.all())

class delall(commands.Cog):
    def __init__ (self, bot: commands.Bot):
        self.bot = bot
        
    @app_commands.command(name="delall")
    @app_commands.default_permissions(administrator=True)
    async def delall(self, interaction: discord.Interaction):

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
        


        guild = interaction.guild
        
        codes_table = f'guild_{guild.id}_Codes'

        cur.execute(f"SELECT CODES FROM {codes_table}")
        all_codes = cur.fetchall()

        cur.execute(f"DELETE FROM {codes_table}", (all_codes))
        con.commit()

        await interaction.response.send_message(
            f"**{interaction.user.name}** alle Codes wurden gelöscht.",
        )
        print(f"ALLE CODES WURDEN GELÖSCHT")
        
        
        con.close()
async def setup(bot):
    await bot.add_cog(delall(bot))
    print('delall cog geladen ✔️')