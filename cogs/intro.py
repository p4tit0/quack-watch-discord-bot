import discord
from discord.ext import commands
from discord.ext.commands import Context
from database.guild_settings import get_guild_settings, update_guild_settings
from database.intro_messages import *
from utils.locales import get_message
import json
import random


class Intro(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    self.colors = [
            discord.Color.teal(),
            discord.Color.dark_teal(),
            discord.Color.green(),
            discord.Color.dark_green(),
            discord.Color.blue(),
            discord.Color.dark_blue(),
            discord.Color.purple(),
            discord.Color.dark_purple(),
            discord.Color.magenta(),
            discord.Color.dark_magenta(),
            discord.Color.gold(),
            discord.Color.dark_gold(),
            discord.Color.orange(),
            discord.Color.dark_orange(),
            discord.Color.red(),
            discord.Color.dark_red(),
            discord.Color.lighter_grey(),
            discord.Color.dark_grey(),
            discord.Color.light_grey(),
            discord.Color.darker_grey(),
            discord.Color.blurple(),
            discord.Color.greyple(),
            discord.Color.dark_theme(),
            discord.Color.random(),
        ]
        
    @commands.has_permissions(administrator=True)
    @commands.command()
    async def setwelcomechannel(self, ctx: Context, channel: discord.TextChannel):
        settings = await get_guild_settings(ctx.guild.id)
        
        # Atualiza o canal de boas-vindas
        settings["welcome_channel_id"] = channel.id
        await update_guild_settings(ctx.guild.id, settings)
        
        await ctx.send(get_message(settings["language"], "welcome_channel_set_success", channel=channel.mention))
    
    @commands.has_permissions(administrator=True)
    @commands.command()
    async def setgoodbyechannel(self, ctx: Context, channel: discord.TextChannel):
        settings = await get_guild_settings(ctx.guild.id)
        
        # Atualiza o canal de despedida
        settings["goodbye_channel_id"] = channel.id
        await update_guild_settings(ctx.guild.id, settings)
        
        await ctx.send(get_message(settings["language"], "goodbye_channel_set_success", channel=channel.mention))

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def setwellcome(self, ctx: Context, channel: discord.TextChannel = None):
        settings = await get_guild_settings(ctx.guild.id)
        
        if not ctx.message.attachments:
            await ctx.send(get_message(settings["language"], "no_file_attached"))
            return
        
        try:
            attachment = ctx.message.attachments[0]
            file_content = await attachment.read()
            embed_data = json.loads(file_content)
            
            if not all(key in embed_data for key in ["title", "description"]):
                await ctx.send(get_message(settings["language"], "embed_missing_fields"))
                return
            
            async with self.bot.pool.acquire() as conn:
                await delete_welcome_messages(conn, ctx.guild.id)
                
                message_id = await insert_welcome_message(conn, ctx.guild.id, embed_data)
                
                if channel is not None:
                    settings["welcome_channel_id"] = channel.id
                settings["welcome_mode"] = "fixed"
                settings["selected_welcome_message_id"] = message_id
                await update_guild_settings(ctx.guild.id, settings)
                
                await ctx.send(get_message(settings["language"], "welcome_set_success"))
        except json.JSONDecodeError:
            await ctx.send(get_message(settings["language"], "invalid_json"))
        except Exception as e:
            await ctx.send(get_message(settings["language"], "welcome_set_error", error=str(e)))

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def setrandomwellcome(self, ctx: Context, channel: discord.TextChannel = None):
        settings = await get_guild_settings(ctx.guild.id)
        
        if not ctx.message.attachments:
            await ctx.send(get_message(settings["language"], "no_file_attached"))
            return
        
        try:
            attachment = ctx.message.attachments[0]
            file_content = await attachment.read()
            embed_list = json.loads(file_content)
            
            if not isinstance(embed_list, list):
                await ctx.send(get_message(settings["language"], "invalid_json_list"))
                return
            
            message_ids = []
            async with self.bot.pool.acquire() as conn:
                await delete_welcome_messages(conn, ctx.guild.id)
                
                for embed_data in embed_list:
                    if not all(key in embed_data for key in ["title", "description"]):
                        await ctx.send(get_message(settings["language"], "embed_missing_fields"))
                        return
                    
                    message_id = await insert_welcome_message(conn, ctx.guild.id, embed_data)
                    message_ids.append(message_id)
                
                if channel is not None:
                    settings["welcome_channel_id"] = channel.id
                settings["welcome_mode"] = "random"
                settings["welcome_message"] = message_ids
                await update_guild_settings(ctx.guild.id, settings)
                
                await ctx.send(get_message(settings["language"], "welcome_set_random_success"))
        except json.JSONDecodeError:
            await ctx.send(get_message(settings["language"], "invalid_json"))
        except Exception as e:
            await ctx.send(get_message(settings["language"], "welcome_set_error", error=str(e)))

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def disablewellcome(self, ctx: Context):
        settings = await get_guild_settings(ctx.guild.id)
        settings["welcome_mode"] = "disabled"
        await update_guild_settings(ctx.guild.id, settings)
        await ctx.send(get_message(settings["language"], "welcome_disabled_success"))

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def setgoodbye(self, ctx: Context, channel: discord.TextChannel = None):
        settings = await get_guild_settings(ctx.guild.id)
        if not ctx.message.attachments:
            await ctx.send(get_message(settings["language"], "no_file_attached"))
            return
        
        try:
            attachment = ctx.message.attachments[0]
            file_content = await attachment.read()
            embed_data = json.loads(file_content)
            
            if not all(key in embed_data for key in ["title", "description"]):
                await ctx.send(get_message(settings["language"], "embed_missing_fields"))
                return
            
            async with self.bot.pool.acquire() as conn:
                await delete_goodbye_messages(conn, ctx.guild.id)
                
                message_id = await insert_goodbye_message(conn, ctx.guild.id, embed_data)
                
                if channel is not None:
                    settings["goodbye_channel_id"] = channel.id
                settings["goodbye_mode"] = "fixed"
                settings["selected_goodbye_message_id"] = message_id
                await update_guild_settings(ctx.guild.id, settings)
                
                await ctx.send(get_message(settings["language"], "goodbye_set_success"))
        except json.JSONDecodeError:
            await ctx.send(get_message(settings["language"], "invalid_json"))
        except Exception as e:
            await ctx.send(get_message(settings["language"], "goodbye_set_error", error=str(e)))

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def setrandomgoodbye(self, ctx: Context, channel: discord.TextChannel = None):
        settings = await get_guild_settings(ctx.guild.id)

        if not ctx.message.attachments:
            await ctx.send(get_message(settings["language"], "no_file_attached"))
            return
        
        try:
            attachment = ctx.message.attachments[0]
            file_content = await attachment.read()
            embed_list = json.loads(file_content)
            
            if not isinstance(embed_list, list):
                await ctx.send(get_message(settings["language"], "invalid_json_list"))
                return
            
            message_ids = []
            async with self.bot.pool.acquire() as conn:
                await delete_goodbye_messages(conn, ctx.guild.id)
                
                for embed_data in embed_list:
                    if not all(key in embed_data for key in ["title", "description"]):
                        await ctx.send(get_message(settings["language"], "embed_missing_fields"))
                        return
                    
                    message_id = await insert_goodbye_message(conn, ctx.guild.id, embed_data)
                    message_ids.append(message_id)
                
                if channel is not None:
                    settings["goodbye_channel_id"] = channel.id
                settings["goodbye_mode"] = "random"
                settings["goodbye_message"] = message_ids
                await update_guild_settings(ctx.guild.id, settings)
                
                await ctx.send(get_message(settings["language"], "goodbye_set_random_success"))
        except json.JSONDecodeError:
            await ctx.send(get_message(settings["language"], "invalid_json"))
        except Exception as e:
            await ctx.send(get_message(settings["language"], "goodbye_set_error", error=str(e)))

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def disablegoodbye(self, ctx: Context):
        settings = await get_guild_settings(ctx.guild.id)
        settings["goodbye_mode"] = "disabled"
        await update_guild_settings(ctx.guild.id, settings)
        await ctx.send(get_message(settings["language"], "goodbye_disabled_success"))

    
        
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        settings = await get_guild_settings(member.guild.id)
        if settings["welcome_mode"] != "disabled" and settings["welcome_channel_id"]:
            channel = self.bot.get_channel(settings["welcome_channel_id"])
            if channel:
                if settings["welcome_mode"] == "fixed":
                    message_id = settings["selected_welcome_message_id"]
                elif settings["welcome_mode"] == "random":
                    message_ids = settings["welcome_message"]
                    message_id = random.choice(message_ids)
                
                async with self.bot.pool.acquire() as conn:
                    embed_data = await conn.fetchrow("""
                        SELECT * FROM welcome_messages WHERE id = $1;
                    """, message_id)
                    
                    if embed_data:
                        embed = self.create_embed(embed_data, member)
                        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        settings = await get_guild_settings(member.guild.id)
        
        if settings["goodbye_mode"] != "disabled" and settings["goodbye_channel_id"]:
            channel = self.bot.get_channel(settings["goodbye_channel_id"])
            if channel:
                if settings["goodbye_mode"] == "fixed":
                    message_id = settings["selected_goodbye_message_id"]
                elif settings["goodbye_mode"] == "random":
                    message_ids = settings["goodbye_message"]
                    message_id = random.choice(message_ids)
                
                async with self.bot.pool.acquire() as conn:
                    embed_data = await conn.fetchrow("""
                        SELECT * FROM goodbye_messages WHERE id = $1;
                    """, message_id)
                    
                    if embed_data:
                        embed = self.create_embed(embed_data, member)
                        await channel.send(embed=embed)

    def create_embed(self, embed_data: dict, member: discord.Member) -> discord.Embed:
        embed = discord.Embed(
            title=self.replace_masks(embed_data["title"], member),
            description=self.replace_masks(embed_data["description"], member),
            color=embed_data["color"] or random.choice(self.colors)
        )
        
        if embed_data["title_url"]:
            embed.url = embed_data["title_url"]
        
        if embed_data["author_name"]:
            embed.set_author(
                name=self.replace_masks(embed_data["author_name"], member),
                url=embed_data["author_url"],
                icon_url=embed_data["author_icon_url"]
            )
        
        if embed_data["fields"]:
            loaded_fields = json.loads(embed_data["fields"])
            for field in loaded_fields:
                embed.add_field(
                    name=self.replace_masks(field["name"], member),
                    value=self.replace_masks(field["value"], member),
                    inline=field.get("inline", False)
                )
        
        if embed_data["image_url"]:
            embed.set_image(url=embed_data["image_url"])
        
        if embed_data["thumbnail_url"]:
            embed.set_thumbnail(url=embed_data["thumbnail_url"])
        
        if embed_data["footer_text"]:
            embed.set_footer(
                text=self.replace_masks(embed_data["footer_text"], member),
                icon_url=embed_data["footer_icon_url"]
            )
        
        if embed_data["timestamp"]:
            embed.timestamp = embed_data["timestamp"]
        
        return embed

    def replace_masks(self, text: str, member: discord.Member) -> str:
        replacements = {
            "{q!username}": member.name,
            "{q!displayname}": member.display_name,
            "{q!mention}": f"<@{member.id}>",
            "{q!profile}": member.avatar.url if member.avatar else member.default_avatar.url,
            "{q!photo}": member.guild.icon.url if member.guild.icon else "",
            "{q!servername}": member.guild.name
        }
        
        for mask, value in replacements.items():
            text = text.replace(mask, value)
        
        return text

async def setup(bot):
    await bot.add_cog(Intro(bot))