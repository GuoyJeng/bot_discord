import discord

from discord.ext import commands
from discord.ui import View

intents = discord.Intents.default()
client = commands.Bot(command_prefix='!', intents=intents)

async def help(interaction: discord.Interaction):
    view = View()

    embed = discord.Embed(
        title=f"{client.user.name} version 0",
        color=discord.Color.magenta(),
    )
    embed.add_field(
        name="Features",
        value= (
            "**/join** \nDescription: Make the bot join your voice channel.\n", 
            "**/leave** \nDescription: Make the bot leave your voice channel.\n", 
            "**/play** \nDescription: Make the bot play a song.\n",
            "**/skip** \nDescription: Skip the current song.\n",
            "**/role** \nDescription: Click to get a role.\n",
            "**/add** \nDescription: Add a question.\n",
            "**/show** \nDescription: List all saved questions.\n",
            "**/delete** \nDescription: Delete a question.\n",)
    )
    
    embed.set_footer(text="Release Date: November 29, 2024")

    await interaction.response.send_message(embed=embed, view=view)
