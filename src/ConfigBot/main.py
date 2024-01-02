import discord
from discord.ext import commands
from discord import app_commands


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.tree.command(name="config")
@app_commands.default_permissions(administrator=True)
async def embed(interaction: discord.Interaction):
    embed = discord.Embed(
        title=f"{bot.user} config Tool", description="This is an example"
    )
    embed.set_author(
        name="MHRRIII",
        url="https://discord.com/users/353999878579290112",
        icon_url="https://cdn.discordapp.com/attachments/1187803260925509804/1187803276951961600/8bJ2lSo.png?ex=65983701&is=6585c201&hm=839ea0432b663b2675f79a2d028cf9c711dc1437232da72271baf28d9e450a4a&",
    )
    embed.set_footer(text="this is the footer")

    await interaction.response.send_message(embed=embed)

    await interaction.response.send_message()

    discord.ui.RoleSelect()

    # EMBEDS 1 MONAT ALT POST https://stackoverflow.com/questions/77398382/discord-py-sending-multiple-embeds
