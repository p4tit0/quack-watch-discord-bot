import os
import json
import discord
from discord.ext import commands
import asyncpg
from google.cloud import secretmanager
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
SECRET_ID = os.getenv("GOOGLE_CLOUD_SECRET_ID")
VERSION = os.getenv("GOOGLE_CLOUD_SECRET_VERSION")

def get_discord_token():
    client = secretmanager.SecretManagerServiceClient()
    secret_name = f"projects/{PROJECT_ID}/secrets/{SECRET_ID}/versions/{VERSION}"
    response = client.access_secret_version(request={"name": secret_name})
    return response.payload.data.decode("UTF-8")

with open("locales.json", "r", encoding="utf-8") as f:
    LOCALES = json.load(f)

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="q!", intents=intents)

POSTGRES_URI = os.getenv("POSTGRES_URI")

async def create_table():
    conn = await asyncpg.connect(POSTGRES_URI)
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS guild_settings (
            guild_id BIGINT PRIMARY KEY,
            language TEXT NOT NULL DEFAULT 'en'
        );
    """)
    await conn.close()

async def get_guild_language(guild_id):
    conn = await asyncpg.connect(POSTGRES_URI)
    row = await conn.fetchrow("""
        SELECT language FROM guild_settings WHERE guild_id = $1;
    """, guild_id)
    await conn.close()
    return row["language"] if row else "en"

async def set_guild_language(guild_id, language):
    conn = await asyncpg.connect(POSTGRES_URI)
    await conn.execute("""
        INSERT INTO guild_settings (guild_id, language)
        VALUES ($1, $2)
        ON CONFLICT (guild_id)
        DO UPDATE SET language = $2;
    """, guild_id, language)
    await conn.close()

def get_message(language, key, **kwargs):
    return LOCALES.get(language, {}).get(key, "Message not found").format(**kwargs)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user} (ID: {bot.user.id})")
    print("Quack Watch está de plantão! 🦆")
    await create_table()

@bot.command()
async def ping(ctx):
    language = await get_guild_language(ctx.guild.id)
    await ctx.send(get_message(language, "ping_response"))

@bot.command()
async def setlang(ctx, language: str):
    if language not in LOCALES:
        await ctx.send(get_message("en", "setlang_invalid", lang=", ".join(LOCALES.keys())))
        return

    await set_guild_language(ctx.guild.id, language)
    await ctx.send(get_message(language, "setlang_success", lang=LOCALES[language]['language']))

@bot.command()
async def lang(ctx):
    language = await get_guild_language(ctx.guild.id)
    await ctx.send(get_message(language, "lang_current", lang=LOCALES[language]['language']))


if __name__ == "__main__":
    token = get_discord_token()
    bot.run(token)