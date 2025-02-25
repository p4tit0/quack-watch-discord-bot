import os
import discord
import asyncpg
from discord.ext import commands
from dotenv import load_dotenv
from database.guild_settings import create_tables, get_guild_settings
from utils.locales import get_message
from utils.secrets import get_secret

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="q!", intents=intents)

COGS_DIR = "cogs"
DEFAULT_COGS = ["config"] 

SECRET_ID = os.getenv("GOOGLE_CLOUD_SECRET_ID_DISCORD")
POSTGRES_URI = os.getenv("POSTGRES_URI")

async def load_cogs():
    for filename in os.listdir(COGS_DIR):
        if filename.endswith(".py") and filename[:-3] in DEFAULT_COGS:
            await bot.load_extension(f"{COGS_DIR}.{filename[:-3]}")

@bot.event
async def on_ready():
    await create_tables()
    bot.pool = await asyncpg.create_pool(POSTGRES_URI)
    for guild in bot.guilds:
        settings = await get_guild_settings(guild.id)
        for cog in settings["loaded_cogs"]:
            try:
                await bot.load_extension(f"cogs.{cog}")
            except Exception as e:
                print(f"Erro ao carregar extensão {cog} para o servidor {guild.id}: {e}")
    
    await load_cogs()
    print(f"Bot conectado como {bot.user} (ID: {bot.user.id})")
    print("Quack Watch está de plantão! 🦆")

if __name__ == "__main__":
    token = get_secret(SECRET_ID)
    bot.run(token)