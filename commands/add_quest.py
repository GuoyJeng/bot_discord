import discord
import json
import asyncio

from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents)

QUESTIONS_FILE = "questions.json"

def ensure_json_file():
    try:
        with open(QUESTIONS_FILE, "r") as file:
            json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(QUESTIONS_FILE, "w") as file:
            json.dump({"questions": []}, file)

def save_question(question):
    ensure_json_file()
    with open(QUESTIONS_FILE, "r") as file:
        data = json.load(file)
    data["questions"].append({"question": question})
    with open(QUESTIONS_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Add a question (interaction-based)
async def add_question(interaction: discord.Interaction, client: discord.Client):
    # Check if the user is an admin
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return

    # Ask the admin for a question
    await interaction.response.defer(ephemeral=True)
    await interaction.followup.send("Please type the question you'd like to save:")

    def check(message: discord.Message):
        return message.author == interaction.user and message.channel == interaction.channel

    try:
        # Wait for the admin's input
        msg = await client.wait_for("message", check=check, timeout=60.0)
        question = msg.content

        # Save the question to the JSON file
        save_question(question)
        await interaction.followup.send(f"The question has been saved: `{question}`")

    except asyncio.TimeoutError:
        await interaction.followup.send("You took too long to respond. Please try again.", ephemeral=True)

# List saved questions
async def list_questions(interaction: discord.Interaction):
    ensure_json_file()
    with open(QUESTIONS_FILE, "r") as file:
        data = json.load(file)

    if not data["questions"]:
        await interaction.response.send_message("No questions have been saved yet.", ephemeral=True)
    else:
        questions = "\n".join(
            [f"{idx + 1}. {q['question']}" for idx, q in enumerate(data["questions"])]
        )
        await interaction.response.send_message(f"Here are the saved questions:\n{questions}", ephemeral=True)
