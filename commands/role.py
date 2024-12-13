import discord

from discord.ext import commands
from discord.ui import Button, View

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='!', intents=intents)

role_name = "✅ verified"

async def on_raw_reaction_add(payload):
    if payload.message_id != payload.message_id:
        return
    
    guild = client.get_guild(payload.guild_id)
    if guild is None:
        return  # Bot is not in the guild
    
    member = guild.get_member(payload.user_id)
    if member is None or member.bot:
        return  # Ignore bots or invalid members
    
    # Get or create the role
    role = discord.utils.get(guild.roles, name=role_name)
    if role is None:
        # If role doesn't exist, create it
        role = await guild.create_role(name=role_name)
        print(f"Created role {role.name}")
    
    # Add the role to the member
    try:
        await member.add_roles(role)
        print(f"Assigned {role.name} to {member.display_name}")
    except discord.Forbidden:
        print(f"Permission error: Can't assign role to {member.display_name}")
    except discord.HTTPException as e:
        print(f"Failed to assign role: {e}")

async def buttonRole_callback(interaction: discord.Interaction):
    guild = interaction.guild

    role = discord.utils.get(guild.roles, name=role_name)
    if role is None:
        role = await guild.create_role(name=role_name)
        print(f"Created role: {role.name}")

    try:
        await interaction.user.add_roles(role)
        await interaction.response.send_message(f"give role {role.name} with {interaction.user.display_name} its done🔥", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("I don't have permission give role to other people.", ephemeral=True)
    except discord.HTTPException as e:
        await interaction.response.send_message(f"An error occurres while granting : {e}", ephemeral=True)

async def role(interaction: discord.Interaction):
    buttonRole = Button(label="✅ verified", style=discord.ButtonStyle.grey)
    buttonRole.callback = buttonRole_callback

    view = View()            
    view.add_item(buttonRole)

    embed = discord.Embed(
            title="You can click the button below to get a role.",
            description="Click ✅ verified button to get a role.",
            color=discord.Color.magenta(),
        )

    message = await interaction.response.send_message(embed=embed, view=view)
   