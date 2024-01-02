import discord
from discord.ext import commands, tasks
from discord import app_commands
import logging
from colorama import Fore
from datetime import datetime
from dotenv import load_dotenv
import os


bot = commands.Bot(command_prefix="&", intents=discord.Intents.all())


class InviteButtons(discord.ui.View):
    def __init__(self, inv: str):
        super().__init__()
        self.inv = inv
        self.add_item(discord.ui.Button(label="Invite Link", url=self.inv))

    @discord.ui.button(label="Invite Btn", style=discord.ButtonStyle.blurple)
    async def inviteBtn(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_message(self.inv)


@bot.command()
async def inv(ctx: commands.Context):
    inv = await ctx.channel.create_invite()
    view = InviteButtons(str(inv))
    await ctx.send("Click below to invite someone", view=view)


bot.run(token="")


"""
    
class InviteButtons(discord.ui.View): 
    def __init__(self, inv: str):
        super().__init__()
        self.inv = inv
        self.add_item(discord.ui.Button(label='Invite Link', url=self.inv))
        
    @discord.ui.button(label='Invite Btn', style=discord.ButtonStyle.blurple)
    async def inviteBtn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(self.inv)

  
@bot.command()
async def invite(ctx: commands.Context):
    inv = await ctx.channel.create_invite()
    view= InviteButtons(str(inv))
    await ctx.send('Click below to invite someone' , view=view) 

"""
