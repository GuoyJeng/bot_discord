import os
import discord

from discord.ext import commands
from discord import Interaction
from discord.ui import View
from discord import FFmpegPCMAudio, opus

from commands.join import join as join_command
from commands.leave import leave as leave_command
from commands.play import play as play_command, skip as skip_command
from commands.role import role as role_command
from commands.help import help as help_command
from commands.add_quest import add_question as add_command, list_questions as show_command
from commands.delete import delete_question as delete_command
from commands.random import send_botton as random_command

token = os.getenv('discord_token')

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

try:
    audio = FFmpegPCMAudio("test.mp3")
    print("FFmpeg is working!")
except Exception as e:
    print(f"FFmpeg error: {e}")

# Check if Opus is installed
if opus.is_loaded():
    print("Opus is loaded and working!")
else:
    print("Opus is not loaded!")

@client.event
async def on_ready():
    await client.tree.sync()
    print(f"Bot is ready as {client.user}")

@client.event
async def on_guild_join(guild):
    embed = discord.Embed(
        title=f"Hellooo I'm {client.user.name} ",
        description=r"I'm a bot to help people who interested in coding to use it more conveniently. And we also have many features to support the use. \n if you want  to know what we can do try using the **\help** command",
        color=discord.Color.green(),
    )
    embed.add_field(
        name=f"Thank you for inviting {client.user.name} to sever ",
        value="If the bot has any problems or malfunctions, you can report to jeng_7 for improvement and correction.",
        inline=False,
    )

    embed.set_footer(text="Release Date: November 20, 2024")

    # Find a suitable text channel to send the message
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            print(f"Sending intro message to heheha")
            await channel.send(embed=embed)
            break

@client.event
async def on_member_join(member):
    print(f"New member joined: {member.display_name}")
    channel = discord.utils.get(member.guild.text_channels, name='𝐖𝐞𝐥𝐜𝐨𝐦𝐞')

    if not channel:
        try:
            channel = await member.guild.create_text_channel(
                name = '𝐖𝐞𝐥𝐜𝐨𝐦𝐞',
                topic = 'welcome new members',
            )
            print(f"'welcome' channel created.")
        except discord.Forbidden:
            print("Permission error: Bot cannot create a channel.")
            return
        except discord.HTTPException as e:
            print(f"HTTP error while creating channel: {e}")
            return
    
    view = View()

    embed = discord.Embed(
        title=f"Welcome {member.display_name} To {member.guild.name} 👋🤓",
        description="Thanks you for joining our server! We hope you have a great time here! :D",
        color=discord.Color.magenta(),
    )
    await channel.send(embed=embed, view=view)

@client.tree.command(name="help", description="show all commands")
async def help(interaction: Interaction):
    await help_command(interaction)

@client.tree.command(name="join", description="Make the bot join your voice channel.")
async def join(interaction: discord.Interaction):
    await join_command(interaction)

@client.tree.command(name="leave", description="Make the bot leave your voice channel.")
async def leave(interaction: Interaction):
    await leave_command(interaction)

@client.tree.command(name="play", description="Make the bot play a song.")
async def play(interaction: discord.Interaction, url: str):
    await play_command(interaction, url)

@client.tree.command(name="skip", description="Skip the current song.")
async def skip(interaction: Interaction):
    await skip_command(interaction)

@client.tree.command(name="role", description="Click to get a role.")
async def role(interaction: discord.Interaction):
    await role_command(interaction)

@client.tree.command(name="add", description="Add a question.")
async def add(interaction: discord.Interaction):
    await add_command(interaction, client)

@client.tree.command(name="show", description="List all saved questions.")
async def show(interaction: discord.Interaction):
    await show_command(interaction)

@client.tree.command(name="delete", description="Delete a question.")
async def delete(interaction: discord.Interaction):
    await delete_command(interaction)

@client.tree.command(name="random", description="Random question.")
async def random(interaction: discord.Interaction):
    await random_command(interaction)

client.run(token)
