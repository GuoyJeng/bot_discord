import discord
import yt_dlp
import logging

from discord.ext import commands
from discord import FFmpegPCMAudio

client = commands.Bot(command_prefix='!', intents=discord.Intents.default())
queue = []

async def play(interaction: discord.Interaction, url: str):
    try:
        logging.debug("Play command invoked.")
        await interaction.response.defer()
        with yt_dlp.YoutubeDL({'format': 'bestaudio', 'noplaylist': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info['title']
      
        vc = interaction.guild.voice_client

        if vc is None:
            if interaction.user.voice:
                channel = interaction.user.voice.channel
                await channel.connect()
            else:
                await interaction.followup.send("Join a voice channel first!")
                return

        if vc.is_playing():
            queue.append(url)
            await interaction.followup.send(f"Add queue: {title}")
        else:
            await play_song(interaction, url)

    except Exception as e:
        await interaction.followup.send(f"An error occurred: {e}")
        return

async def play_song(interaction: discord.Interaction, url: str):
    vc = interaction.guild.voice_client

    try:
        with yt_dlp.YoutubeDL({'format': 'bestaudio', 'noplaylist': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info['url']
            title = info['title']

        #ตรงส่วนนี้ทำให้บอทสามารถเล่นเพลงอันต่อไปได้
        def play_next(_):
            if queue:
                next_url = queue.pop(0)
                client.loop.create_task(play_song(interaction, next_url))
            else:
                client.loop.create_task(interaction.followup.send(f"No more songs in the queue,I'm leaving voice channel!"))
                client.loop.create_task(vc.disconnect())

        vc.play(FFmpegPCMAudio(audio_url), after=play_next)
        await interaction.followup.send(f"Now playing: {title}")

    except Exception as e:
        await interaction.followup.send(f"An error occurred: {e}")
