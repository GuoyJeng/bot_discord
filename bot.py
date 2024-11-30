import os
import discord
import yt_dlp
import asyncio
import random
import json
import uvicorn
import logging
import requests
import secrets
import logging

from dotenv import load_dotenv
from discord.ext import commands
from discord import Interaction
from discord import FFmpegPCMAudio
from discord import app_commands
from discord.ui import Button, View
from discord import utils
from pymongo import MongoClient
from threading import Thread
from pydantic import BaseModel
from typing import Optional