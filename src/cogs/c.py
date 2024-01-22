import discord
from discord.ext import commands
from discord import app_commands
import mariadb
import sys


bot = commands.Bot(command_prefix="&", intents=discord.Intents.all())


class c(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @app_commands.command(name="c", description='show all valid codes')
    @app_commands.default_permissions(administrator=True)
    async def codes(self, interaction: discord.Interaction):
        
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
                
        
        guild = interaction.guild

        codes_table = f'guild_{guild.id}_Codes'
        cur.execute(f"SELECT CODES FROM {codes_table}")
        all_codes = cur.fetchall()
        sanitized_all_codes = [str(x[0]) for x in all_codes]
        
        print(f"{interaction.user} hier sind alle Codes: \n{sanitized_all_codes}")

        await interaction.response.send_message(
            f"**{interaction.user}** hier sind alle Codes: `\n{sanitized_all_codes}`",
            ephemeral=True,
        )

            #if not interaction.user._permissions.:
            #   interaction.response.send_message("Stop being naughty")

        con.close()
async def setup(bot):
    await bot.add_cog(c(bot))
    print("c cog geladen ✔️")
