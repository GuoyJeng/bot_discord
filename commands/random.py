import discord
import random
import json

from discord.ext import commands
from discord.ui import Button, View

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

with open('questions.json', 'r') as file:
    data = json.load(file)

async def send_botton(interaction: discord.Interaction):
    view = View()
    button = Button(label="Click", style=discord.ButtonStyle.success, custom_id="button1")
    
    async def button_callback(interaction: discord.Interaction):
        question = random.choice(data['questions'])
        await interaction.response.send_message(question['question'], ephemeral=True)

    embed = discord.Embed(
            title="Random question",
            description="It will send you a random question.",
            color=discord.Color.magenta(),
        )

    button.callback = button_callback
    view.add_item(button)

    await interaction.response.send_message(embed=embed, view=view)
