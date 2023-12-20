import discord
from discord.ext import commands , tasks
from discord import app_commands
import logging
from colorama import Fore
from datetime import datetime 
from dotenv import load_dotenv
import os


load_dotenv()
token = str(os.getenv("TOKEN"))


bot = commands.Bot(command_prefix='!' , intents= discord.Intents.all())

# Logging Handler to log info 
handler = logging.FileHandler(filename='discordPY.log', encoding='utf-8', mode  = 'w')


@bot.event    
async def on_ready():
    print(f'{bot.user} is ready to rumble!')
    print('Published by Moritz Reiswaffel')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} commands!')
    except Exception as e:
        print(e)
    print('------------------------------')    
    
    
# Globale variablen für z.B. die Codes Data Liste 
# Oder Sachen die immer wieder vorkommen z.B. dt_string
DATA = []
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")


# Geht nicht wieso ? 

# @bot.event
# async def on_message(message, interaction: discord.Interaction):
#     if message.content == '.sync' and message.author.has_permissions(administrator=True):
#             if interaction.user.id == 353999878579290112:
#                 await bot.tree.sync()
#                 print('Command tree synced.')
#             else:
#                 await interaction.response.send_message('You must be the owner to use this command!')

# Lässt user einen Code für of Rolle erstellen 
# Code wird in DATA und .txt file gespeichert

@bot.tree.command(name='makeof' , description='Make OF code. Only for Admins')
@commands.has_permissions(administrator=True)
@app_commands.describe(arg_of = 'Wie soll der Code sein ? ')
async def pwd(interaction: discord.Interaction, arg_of: str):
    Codes  = open('Codes.txt' , 'a')
    await interaction.response.send_message(f'Ok, **{interaction.user.name}** der Code für die Onlyfans Rolle ist jetzt: `{arg_of}`')

    DATA.append(arg_of)
    print('Onlyfans Code: ' + arg_of)
    
    Codes.writelines(f'Onlyfans Code: {arg_of}\n')
    Codes.close()



# Gleicher Command nur für bf Rolle
@bot.tree.command(name='makebf' , description='Make BF code. Only for Admins')
@commands.has_permissions(administrator=True)
@app_commands.describe(arg_bf = 'Wie soll der Code sein ? ')
async def code(interaction: discord.Interaction, arg_bf: str):
    Codes  = open('Codes.txt' , 'a')
    await interaction.response.send_message(f'Ok, **{interaction.user.name}** der Code für die Bestfans Rolle ist jetzt: `{arg_bf}`')
# Schreibt input (arg_bf) in die DATA Liste und printet auf console
    DATA.append(arg_bf)
    print('Bestfans Code: ' + arg_bf)

# Schreibt input (arg_bf) in .txt file
    Codes.writelines(f'Bestfans Code: {arg_bf}\n')
    Codes.close() 





# code aus makeof kann hier genutzt werden um sich die Rolle zu geben. Der Input wird mit der Liste DATA abgegelichen bzw mit dem .txt file
# Darauf hin wird die Rolle gegeben oder nicht
# Ausserdem wird in einem .txt file gelogged wer und wann eine Rolle bekommen hat

@bot.tree.command(name='of_sub' , description='Enter the code you got to claim your Onlyfans role.')
@app_commands.describe(input = 'Wie lautet der Code ?')
async def eingabe(interaction: discord.Interaction, input: str):
    sc = open('Codes.txt' , 'r')
    scContent = sc.read()
    user = interaction.user
    CodeLogs = open('CodeLogs.txt', 'a')
    RoleLogs = open('RoleLogs.txt', 'a')
    if input in scContent:
        await interaction.response.send_message(f'**{interaction.user.name}** du hast den richtigen Code eingegeben. Hier ist deine Rolle.')
        
        guild = interaction.guild
        role_Onlyfans = discord.utils.get(guild.roles, name='OnlyFans Sub')
        await user.add_roles(role_Onlyfans)

        print(f'Added role {role_Onlyfans} to {user}')
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print(f'{user} hat einen Code eingelöst: {input} :: {dt_string}\n')
        CodeLogs.writelines(f'{user} ({user.id}) hat einen Code eingelöst: {role_Onlyfans} :: {input} :: {dt_string}\n')
        RoleLogs.writelines(f'Added role {role_Onlyfans} to {user} ({user.id}) :: {dt_string}\n')
        RoleLogs.close()
        sc.close()        
    else:
        await interaction.response.send_message(f'*{interaction.user.name}* du hast den falschen Code eingegeben')




# code aus makebf kann hier genutzt werden um sich die Rolle zu geben. Der Input wird mit der Liste DATA abgegelichen bzw mit dem .txt file
# Darauf hin wird die Rolle gegeben oder nicht
# Ausserdem wird in einem .txt file gelogged wer und wann eine Rolle bekommen hat

@bot.tree.command(name='bf_sub', description='Enter the code you got to claim your Bestfans role.')
@app_commands.describe(input = 'Wie lautet der Code ?')
async def eingabe(interaction: discord.Interaction, input: str):
    sc = open('Codes.txt' , 'r')
    scContent = sc.read()
    user = interaction.user
    CodeLogs = open('CodeLogs.txt', 'a')
    RoleLogs = open('RoleLogs.txt', 'a')
    if input in scContent:
        guild = interaction.guild
        role_bestfans = discord.utils.get(guild.roles, name='Bestfans Sub')
        await user.add_roles(role_bestfans)
        
        #if role_bestfans in user.roles:
        await interaction.response.send_message(f'**{interaction.user.name}** du hast den richtigen Code eingegeben. Hier ist deine Rolle.')
            
        print(f'Added role {role_bestfans} to {user}')
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print(f'{user} hat einen Code eingelöst: {input} :: {dt_string}\n')
        CodeLogs.writelines(f'{user} ({user.id}) hat einen Code eingelöst: {role_bestfans} :: {input} :: {dt_string}\n')
        RoleLogs.writelines(f'Added role {role_bestfans} to {user} ({user.id}) :: {dt_string}\n')
        RoleLogs.close()
        sc.close()
    else:
        await interaction.response.send_message(f'*{interaction.user.name}* du hast den falschen Code eingegeben')
        
                

 
 
 
        
# Hier kann man die Codes die festegelegt wurden wieder löschen, der Bot greift auf beide .txt files zu um zu schauen ob es den Code gibt
# Und zu welcher Rolle of oder bf er gehört.


@bot.tree.command(name='delete')
@commands.has_permissions(administrator=True)
@app_commands.describe(input_one = 'Delete either a Bestfans or Onlyfans claim code.')
async def delete_code(interaction: discord.Interaction, input_one: str): 
    sc = open('Codes.txt' , 'r')
    file_path = 'Codes.txt'

    with open(file_path, 'r') as file:
        lines = file.readlines()

    updated_lines = [line.strip() for line in lines if input_one not in line]

    with open(file_path, 'w') as file:
        file.write('\n'.join(updated_lines))

    if len(lines) != len(updated_lines):
        scContent = sc.read()
        await interaction.response.send_message(f'Ok, **{interaction.user.name}** der Code `{input_one}` wurde gelöscht. \n Folgende Codes sind noch aktiv: `{scContent}`')
        print(f'Code {input_one} wurde gelöscht')
        

    else: 
        await interaction.response.send_message(f'Blöd gelaufen, **{interaction.user.name}** der Code `{input_one}` existiert nicht')
        print(f'Code {input_one} existiert nicht')



@bot.tree.command(name='delall')
@commands.has_permissions(administrator=True)
@app_commands.describe(input = '"all" to delete all codes')
async def delall(interaction: discord.Interaction, input:str): 
    if input == 'all':
        sc = open('Codes.txt' , 'w')
        await interaction.response.send_message(f'**{interaction.user.name}** hat alle gültigen codes gelöscht')
        print(Fore.RED + f'{interaction.user.name} hat alle codes gelöscht :: {dt_string}')
        sc.close()

    else: 
        await interaction.response.send_message('This was not the right keyword. Please enter "all" to delete all codes.')

# Zeigt alle codes an die gerade valide sind
@bot.event
async def on_message (message): 
    sc = open('Codes.txt' , 'r') 
    scContent = sc.read()  
    if message.content == '.code':
            print(f'{message.author} hier sind alle Codes: {scContent}')
            # read from file and print output      
            await message.reply(f'**{message.author}** hier sind alle Codes: `\n{scContent}`')
            sc.close()
    #else: 
    #    await message.reply(f'{message.author} STOP. Dazu hast du keine Berechtigung')



bot.run(token , log_handler=handler)