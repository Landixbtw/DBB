import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from dateutil.relativedelta import relativedelta
import mariadb
import sys



bot = commands.Bot(command_prefix="&", intents=discord.Intents.all())


class makeof(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="makeof", description="Make an Onlyfans code. Only for Admins"
    )
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(arg="Wie soll der code sein ?")
    async def codeOF(self, interaction: discord.Interaction, arg: str):
        await interaction.response.send_message(
            f"Ok, **{interaction.user.name}** Code für die Onlyfans Rolle: `{arg}`",
            ephemeral=True,
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

        guild = interaction.guild
        
        codes_table = f'{guild.id}_Codes'
        
        one_month_from_now = datetime.now() + relativedelta(months=1)

        cur.execute(f'INSERT INTO guild_{codes_table} VALUES (?, ?, ?)', ["O", arg, one_month_from_now.strftime("%Y-%m-%d %H:%M:%S")])
        
        con.commit()
        con.close()

async def setup(bot):
    await bot.add_cog(makeof(bot))
    print("makeof cog geladen ✔️")
