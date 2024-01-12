import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from dateutil.relativedelta import relativedelta
import mariadb
import sys


bot = commands.Bot(command_prefix="&", intents=discord.Intents.all())


class bf_sub(commands.Cog): 
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @app_commands.command(
        name="bf_sub", description="Enter the code you got to claim your Bestfans role."
    )
    @app_commands.describe(input="Wie lautet der Code ?")
    async def eingabe(self, interaction: discord.Interaction, input: str):
        
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
        
        user = interaction.user
        guild = interaction.guild

        codes_table = f"guild_{guild.id}_Codes"

        cur.execute(f"SELECT CODES from {codes_table}")
        content = cur.fetchall()
        cur.execute(f"SELECT USE_CASE FROM {codes_table}")
        use_case = cur.fetchall()


        cur.execute(f"SELECT CODES FROM {codes_table} WHERE CODES=?", (input,))
        result = cur.fetchone()
                
        role_Bestfans = discord.utils.get(guild.roles, name="Bestfans Sub")
            
        redeem_logs_table = f"guild_{guild.id}_CodeRedeemLogs"
        role_receive_logs_table = f"guild_{guild.id}_RoleReceiveLogs"
        
        
        sanitized_content = [str(x[0]) for x in content]
        sanitized_use_case = [str(x[0]) for x in use_case]

        if input in sanitized_content and sanitized_use_case:                    
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

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            cur.execute(f"INSERT INTO {role_receive_logs_table} VALUES (?, ?, ?, ?)", [user.name, "B", user.id, now])
            
            cur.execute(f"INSERT INTO {redeem_logs_table} VALUES (?, ?, ?)", [user.name, input, now])

            con.commit()

            async def date_handler():
                cur.execute(f"SELECT REDEEMED_AT FROM {redeem_logs_table}")
                date = cur.fetchone()[0]
                print(date)

                if role_Bestfans in user.roles and date == now:
                    # wenn user rolle hat und date == now entspricht rolle weg.
                    user.remove_roles(role_Bestfans)
                    DM = await bot.fetch_user(interaction.user.id)
                    await DM.send(
                        "1 Month is over, and your Bestfans or Onlyfans role has been taken away, if you want the role again and can prove that you have a **valid subscription** of either, open a Ticket on the 'I have a question' Ticket and send a screenshot of privatebunnys respective profile so that we can see you are subscribed. "
                    )

            await date_handler()
    
        else:
            await interaction.response.send_message(
            f"*{interaction.user.name}* du hast den falschen Code eingegeben"
                    )    
        con.close()
    


async def setup(bot): 
    await bot.add_cog(bf_sub(bot))
    print('bf_sub cog geladen ✔️')