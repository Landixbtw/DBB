from datetime import datetime
from dateutil.relativedelta import relativedelta
#from Database.dbmain import DatabaseConnection as con
import discord

class codes_perm(): 
    def __init__(self, code):
        self.code = code
    
    # async def user_interaction(interaction: discord.Interaction, arg_of: str):
    #     await interaction.response.send_message(f"Ok, **{interaction.user.name}** Code für die Onlyfans Rolle: `{arg_of}`",ephemeral=True,)
        
        
    def log_to_file():
        CODES_FILE_PATH = "src/dotxml/Codes.xml"
        Codes = open(CODES_FILE_PATH, "a")
        Codes.writelines(f'Onlyfans Code: {arg_of}\n')
        Codes.close()
        
    def write_to_DB():
        DATA = []
        DATA.append("Onlyfans")
        DATA.append("test")
        
        one_month_from_now = datetime.now() + relativedelta(months=1) 
        DATA.append(one_month_from_now.strftime("%H:%M:%S %d/%m/%Y"))       
        
        print(DATA)
        
        # cur.execute("INSERT INTO codes (Plattform, Codes, `Gueltig bis`) VALUES ( ?, ?, ?)", (DATA))
        # print('test 1')
        # con.commit()
        # print('test 2')
        # con.close()
        # print('code passed to database')
