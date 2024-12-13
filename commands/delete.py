import discord
import json
import asyncio

from discord.ext import commands

from commands.add_quest import ensure_json_file

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents)

QUESTIONS_FILE = "questions.json"

async def delete_question(interaction: discord.Interaction):
    ensure_json_file()
    with open(QUESTIONS_FILE, "r") as file:
        data = json.load(file)

    # Check if there are any questions to delete
    if not data["questions"]:
        await interaction.response.send_message("No questions have been saved yet.", ephemeral=True)
        return

    # Show the list of questions and ask the admin which one to delete
    questions = "\n".join(
        [f"{idx + 1}. {q['question']}" for idx, q in enumerate(data["questions"])]
    )
    await interaction.response.defer(ephemeral=True)
    await interaction.followup.send(
        f"Here are the saved questions:\n{questions}\n\nType the number of the question you'd like to delete:"
    )

    def check(message: discord.Message):
        return message.author == interaction.user and message.channel == interaction.channel

    try:
        # Wait for the admin's input
        msg = await interaction.client.wait_for("message", check=check, timeout=30.0)
        index = int(msg.content) - 1  # Convert input to a list index

        if 0 <= index < len(data["questions"]):
            deleted_question = data["questions"].pop(index)  # Remove the question
            with open(QUESTIONS_FILE, "w") as file:
                json.dump(data, file, indent=4)
            await interaction.followup.send(f"Question deleted: `{deleted_question['question']}`")
        else:
            await interaction.followup.send("Invalid number. Please try again.", ephemeral=True)

    except ValueError:
        await interaction.followup.send("Invalid input. Please enter a number.", ephemeral=True)
    except asyncio.TimeoutError:
        await interaction.followup.send("You took too long to respond. Please try again.", ephemeral=True)
