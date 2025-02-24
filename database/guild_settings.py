import asyncpg
from dotenv import load_dotenv
import os
import json

load_dotenv()

POSTGRES_URI = os.getenv("POSTGRES_URI")

async def create_tables():
    conn = await asyncpg.connect(POSTGRES_URI)
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS guild_settings (
            guild_id BIGINT PRIMARY KEY,
            enabled_cogs TEXT[] NOT NULL DEFAULT '{}',
            language TEXT NOT NULL DEFAULT 'en_us',
            loaded_cogs TEXT[] NOT NULL DEFAULT '{}'            
        );
    """)
    await conn.close()

async def get_guild_settings(guild_id):
    conn = await asyncpg.connect(POSTGRES_URI)
    row = await conn.fetchrow("""
        SELECT * FROM guild_settings WHERE guild_id = $1;
    """, guild_id)
    await conn.close()
    return row if row else {"guild_id": guild_id, "enabled_cogs": [], "language": "en_us", "loaded_cogs": []}


async def update_guild_settings(guild_id, settings):
    conn = await asyncpg.connect(POSTGRES_URI)
    await conn.execute("""
        INSERT INTO guild_settings (guild_id, enabled_cogs, language, loaded_cogs)
        VALUES ($1, $2, $3, $4)
        ON CONFLICT (guild_id)
        DO UPDATE SET enabled_cogs = $2, language = $3, loaded_cogs = $4;
    """, guild_id, settings["enabled_cogs"], settings["language"], settings["loaded_cogs"])
    await conn.close()