import discord

async def skip(interaction: discord.Interaction):
    if interaction.guild.voice_client is None:
        await interaction.response.send_message("You haven't invited me to join a voice channel 😫")
        return

    if interaction.guild.voice_client.is_playing():
        interaction.guild.voice_client.stop() 
        await interaction.response.send_message("Song skipped!")
    else:
        await interaction.response.send_message("There are no songs to skip :P.") 
