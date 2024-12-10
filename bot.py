import os
import discord

from discord.ext import commands
from discord import Interaction
from discord.ui import View

from commands.join import join as join_command
from commands.leave import leave as leave_command
from commands.play import play as play_command
from commands.skip import skip as skip_command
from commands.role_com import role as role_command
from commands.help import help as help_command

token = os.getenv('discord_token')

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

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
    # Send a welcome message in the default text channel or a specific channel
    channel = discord.utils.get(member.guild.text_channels, name='welcome')

    if channel:
        view = View()

        embed = discord.Embed(
            title=f"Welcome {member.display_name} To {member.guild.name} 👋🤓",
            description="Thanks you for joining our server! We hope you have a great time here! :D",
            color=discord.Color.blue(),
        )
        await channel.send(embed=embed, view=view)
    else:
        print("Default text channel not found.")

@client.tree.command(name="help", description="Replies with pong!")
async def help(interaction: Interaction):
    await help_command(interaction)

@client.tree.command(name="join", description="Replies with pong!")
async def join(interaction: discord.Interaction):
    await join_command(interaction)

@client.tree.command(name="leave", description="Replies with pong!")
async def leave(interaction: Interaction):
    await leave_command(interaction)

@client.tree.command(name="play", description="Replies with pong!")
async def play(interaction: discord.Interaction, url: str):
    await play_command(interaction, url)

@client.tree.command(name="skip", description="Replies with pong!")
async def skip(interaction: Interaction):
    await skip_command(interaction)

@client.tree.command(name="role", description="Replies with pong!")
async def role(interaction: discord.Interaction):
    await role_command(interaction)

client.run(token)
