import asyncpg
from dotenv import load_dotenv
import os
import json

load_dotenv()

POSTGRES_URI = os.getenv("POSTGRES_URI")

async def create_tables():
    conn = await asyncpg.connect(POSTGRES_URI)
    with open("database/create_db.sql", "r", encoding="utf-8") as f:
        await conn.execute(f.read())
    await conn.close()

async def get_guild_settings(guild_id):
    conn = await asyncpg.connect(POSTGRES_URI)
    row = await conn.fetchrow("""
        SELECT * FROM guild_settings WHERE guild_id = $1;
    """, guild_id)
    await conn.close()

    if row:
        return dict(row)
    else:
        return {
            "guild_id": guild_id,
            "enabled_cogs": [],
            "language": "en_us",
            "loaded_cogs": [],
            "welcome_channel_id": None,
            "welcome_mode": "disabled",
            "selected_welcome_message_id": None,
            "goodbye_channel_id": None,
            "goodbye_mode": "disabled",
            "selected_goodbye_message_id": None,
            "rules_channel_id": None,
            "rules_message": None,
            "rules_required": False,
            "intro_channel_id": None,
            "intro_template": None,
            "intro_questions": None,
            "custom_roles_enabled": False
        }


async def update_guild_settings(guild_id, settings):
    conn = await asyncpg.connect(POSTGRES_URI)
    await conn.execute("""
        INSERT INTO guild_settings (
            guild_id, enabled_cogs, language, loaded_cogs,
            welcome_channel_id, welcome_mode, selected_welcome_message_id,
            goodbye_channel_id, goodbye_mode, selected_goodbye_message_id,
            rules_channel_id, rules_message, rules_required,
            intro_channel_id, intro_template, intro_questions,
            custom_roles_enabled
        ) VALUES (
            $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17
        )
        ON CONFLICT (guild_id)
        DO UPDATE SET
            enabled_cogs = $2,
            language = $3,
            loaded_cogs = $4,
            welcome_channel_id = $5,
            welcome_mode = $6,
            selected_welcome_message_id = $7,
            goodbye_channel_id = $8,
            goodbye_mode = $9,
            selected_goodbye_message_id = $10,
            rules_channel_id = $11,
            rules_message = $12,
            rules_required = $13,
            intro_channel_id = $14,
            intro_template = $15,
            intro_questions = $16,
            custom_roles_enabled = $17;
    """, guild_id,
        settings.get("enabled_cogs", []),
        settings.get("language", "en_us"),
        settings.get("loaded_cogs", []),
        settings.get("welcome_channel_id"),
        settings.get("welcome_mode", "disabled"),
        settings.get("selected_welcome_message_id"),
        settings.get("goodbye_channel_id"),
        settings.get("goodbye_mode", "disabled"),
        settings.get("selected_goodbye_message_id"),
        settings.get("rules_channel_id"),
        settings.get("rules_message"),
        settings.get("rules_required", False),
        settings.get("intro_channel_id"),
        settings.get("intro_template"),
        settings.get("intro_questions"),
        settings.get("custom_roles_enabled", False)
    )
    await conn.close()