import discord

from discord.ui import View

intents = discord.Intents.default()

async def help(interaction: discord.Interaction):
    view = View()

    embed = discord.Embed(
        title="Bot for coding version 0",
        color=discord.Color.blue(),
    )
    embed.add_field(
        name="Features",
        value= "**/practice** \nDescription: Show a coding question.\n **/join** \nDescription: Make the bot join your voice channel.\n **/leave** \nDescription: Make the bot leave your voice channel.\n **/play** \nDescription: Make the bot play a song.\n **/skip** \nDescription: Skip the current song.\n **/last_question** \nDescription: Show the last question.",
        inline=False,
    )
    
    embed.set_footer(text="Release Date: November 29, 2024")

    await interaction.response.send_message(embed=embed, view=view)
