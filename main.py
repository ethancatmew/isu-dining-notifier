import discord
import aiosqlite
import os
from dotenv import load_dotenv
from discord.ext import commands

bot = commands.Bot(command_prefix = '$', intents = discord.Intents.all())
load_dotenv()

@bot.event
async def on_ready():
    sync = await bot.tree.sync()
    await bot.change_presence(status = discord.Status.idle)
    print(f'{bot.user} is now online, synced {len(sync)} commands.')

@bot.event
async def on_app_command_error(interaction, error):
    print(repr(error))

bot.run(os.getenv("DISCORD_BOT"))