import asyncpg
import json
from typing import List, Dict, Any
from datetime import datetime

async def delete_welcome_messages(conn: asyncpg.Connection, guild_id: int):
    await conn.execute("DELETE FROM welcome_messages WHERE guild_id = $1;", guild_id)

async def delete_goodbye_messages(conn: asyncpg.Connection, guild_id: int):
    await conn.execute("DELETE FROM goodbye_messages WHERE guild_id = $1;", guild_id)

async def insert_welcome_message(conn: asyncpg.Connection, guild_id: int, embed_data: Dict[str, Any]) -> int:
    result = await conn.fetchrow("""
        INSERT INTO welcome_messages (
            guild_id, title, description, title_url, color, author_name,
            author_url, author_icon_url, fields, image_url, thumbnail_url,
            footer_text, footer_icon_url, timestamp
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)
        RETURNING id;
    """, guild_id, embed_data.get("title"), embed_data.get("description"),
        embed_data.get("title_url"), embed_data.get("color"), embed_data.get("author_name"),
        embed_data.get("author_url"), embed_data.get("author_icon_url"), json.dumps(embed_data.get("fields")),
        embed_data.get("image_url"), embed_data.get("thumbnail_url"), embed_data.get("footer_text"),
        embed_data.get("footer_icon_url"), datetime.strptime(embed_data.get("timestamp"), "%Y-%m-%dT%H:%M:%S.%f%z"))
    return result["id"]

async def insert_goodbye_message(conn: asyncpg.Connection, guild_id: int, embed_data: Dict[str, Any]) -> int:
    result = await conn.fetchrow("""
        INSERT INTO goodbye_messages (
            guild_id, title, description, title_url, color, author_name,
            author_url, author_icon_url, fields, image_url, thumbnail_url,
            footer_text, footer_icon_url, timestamp
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)
        RETURNING id;
    """, guild_id, embed_data.get("title"), embed_data.get("description"),
        embed_data.get("title_url"), embed_data.get("color"), embed_data.get("author_name"),
        embed_data.get("author_url"), embed_data.get("author_icon_url"), json.dumps(embed_data.get("fields")),
        embed_data.get("image_url"), embed_data.get("thumbnail_url"), embed_data.get("footer_text"),
        embed_data.get("footer_icon_url"), datetime.strptime(embed_data.get("timestamp"),"%Y-%m-%dT%H:%M:%S.%f%z"))
    return result["id"]