import discord

intents = discord.Intents.default()
intents.members = True

async def join(interaction: discord.Interaction):
    if interaction.user.voice is None:
        await interaction.response.send_message("You haven't invited me to a voice chat!", ephemeral=True)
        return
    
    channel = interaction.user.voice.channel
    
    await channel.connect()
    await interaction.response.send_message(f"join voice channel {channel} done!")
