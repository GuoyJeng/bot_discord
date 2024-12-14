import discord
import yt_dlp
import logging

from discord.ext import commands
from discord import FFmpegPCMAudio

client = commands.Bot(command_prefix='!', intents=discord.Intents.default())
queue = []

# โหลดตัว opus เพื่อทำให้บอทเล่นเพลงได้
discord.opus.load_opus('/opt/homebrew/lib/libopus.dylib')

async def play(interaction: discord.Interaction, url: str):
    try:
        await interaction.response.defer()

        # ดาวน์โหลดเพลง
        with yt_dlp.YoutubeDL({'format': 'bestaudio', 'noplaylist': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info['title']
            audio_url = info['url']

        vc = interaction.guild.voice_client
        if vc is None:  
            if interaction.user.voice:  
                channel = interaction.user.voice.channel
                vc = await channel.connect()  
            else:
                await interaction.followup.send("You must join a voice channel first!")
                return

        if vc.is_playing():  
            queue.append((audio_url, title))
            await interaction.followup.send(f"Added to queue: {title}")
        else:  
            await play_song(vc, interaction, audio_url, title)

    except Exception as e:
        await interaction.followup.send(f"An error occurred: {e}")

async def play_song(vc, interaction, audio_url, title):
    async def play_next_song(_):
        if queue:
            next_audio_url, next_title = queue.pop(0)
            await play_song(vc, interaction, next_audio_url, next_title)
        else:
            await vc.disconnect()

    def play_next_song_callback(_):
        client.loop.create_task(play_next_song(vc))
        return

    try:
        logging.info(f"Now playing: {title} - {audio_url}")

        source = FFmpegPCMAudio(audio_url)
        vc.play(source, after=play_next_song_callback)
        await interaction.followup.send(f"Now playing: {title}")

    except discord.ClientException as e:
        await interaction.followup.send(f"Client error while playing: {e}")
    except discord.OpusNotLoaded:
        await interaction.followup.send("Opus library is not loaded. Make sure Opus is installed.")
    except Exception as e:
        await interaction.followup.send(f"An error occurred while playing: {e}")

async def skip(vc, interaction: discord.Interaction):
    if vc is None:
        await interaction.response.send_message("You haven't invited me to join a voice channel 😫")
        return

    if vc and vc.is_playing():
        vc.stop() 
        await interaction.response.send_message("Song skipped!")
        if queue:
            next_audio_url, next_title = queue.pop(0)
            await play_song(vc, interaction, next_audio_url, next_title)
        else:
            await vc.disconnect()
    else:
        await interaction.response.send_message("There are no songs to skip :P.") 
