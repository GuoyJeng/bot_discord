import discord

intents = discord.Intents.default()
intents.members = True

async def leave(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if voice_client:
        await voice_client.disconnect()
        await interaction.response.send_message("leave voice channel!")
    else:
        await interaction.response.send_message("You haven't invited me to join a voice channel 😫")
