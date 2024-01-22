import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from dateutil.relativedelta import relativedelta
import mariadb
import sys


bot = commands.Bot(command_prefix="&", intents=discord.Intents.all())


class makebf(commands.Cog):
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
        """
        Input von user (arg_bf) wird in .txt file src/dotxml/Codes.xml gespeichert. Sodass code genutzt werden kann auch wenn der Bot neugestartet wird. 
        """
        codes_table = f"{guild.id}_Codes"
        redeem_logs_table = f"{guild.id}_CodeRedeemLogs"
        role_receive_logs_table = f"{guild.id}_RoleReceiveLogs"        
        
        one_month_from_now = datetime.now() + relativedelta(months=1)

        cur.execute(f"INSERT INTO guild_{codes_table} VALUES (?, ?, ?)", ["B", arg_bf, one_month_from_now.strftime("%Y-%m-%d %H:%M:%S")])
        
        
        con.commit()
        con.close()

async def setup(bot):
    await bot.add_cog(makebf(bot))
    print("makebf cog geladen ✔️")
