import discord
from discord.ext import commands
from discord import app_commands
import mariadb
import sys


bot = commands.Bot(command_prefix="&", intents=discord.Intents.all())


class delete(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        
    @app_commands.command(name="delete")
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(input="Delete a code")
    async def delete_code(self, interaction: discord.Interaction, input: str):
        
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

        sanitized_list = [str(x[0]) for x in all_codes]

        if input in sanitized_list:
            cur.execute(f"DELETE FROM {codes_table} WHERE CODES = ?", (input,))
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
async def setup(bot):
    await bot.add_cog(delete(bot))
    print('delete cog geladen ✔️')
    