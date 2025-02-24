import os
import discord
from discord.ext import commands
from discord.ext.commands import Context
from database.guild_settings import get_guild_settings, update_guild_settings
from utils.locales import get_message

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Comando: q!load <cog>
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def load(self, ctx: Context, cog: str = None):
        settings = await get_guild_settings(ctx.guild.id)
        
        if cog is None:
            await ctx.send(get_message(settings["language"], "help_load"))
            return
        
        try:
            await self.bot.load_extension(f"cogs.{cog}")
            if cog not in settings["loaded_cogs"]:
                settings["loaded_cogs"].append(cog)
                await update_guild_settings(ctx.guild.id, settings)
            await ctx.send(get_message(settings["language"], "load_success", cog=cog))
        except Exception as e:
            await ctx.send(get_message(settings["language"], "load_error", cog=cog, error=str(e)))

    # Comando: q!unload <cog>
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unload(self, ctx: Context, cog: str = None):
        settings = await get_guild_settings(ctx.guild.id)
        
        if cog is None:
            await ctx.send(get_message(settings["language"], "help_unload"))
            return
        
        try:
            if cog == 'config':
                await ctx.send(get_message(settings["language"], "unload_config"))
                return
            await self.bot.unload_extension(f"cogs.{cog}")
            if cog in settings["loaded_cogs"]:
                settings["loaded_cogs"].remove(cog)
                await update_guild_settings(ctx.guild.id, settings)
            await ctx.send(get_message(settings["language"], "unload_success", cog=cog))
        except Exception as e:
            await ctx.send(get_message(settings["language"], "unload_error", cog=cog, error=str(e)))

    # Comando: q!reload <cog>
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reload(self, ctx: Context, cog: str = None):        
        settings = await get_guild_settings(ctx.guild.id)
        if cog is None:
            await ctx.send(get_message(settings["language"], "help_reload"))
            return
        try:
            await self.bot.reload_extension(f"cogs.{cog}")
            await ctx.send(get_message(settings["language"], "reload_success", cog=cog))
        except Exception as e:
            await ctx.send(get_message(settings["language"], "reload_error", cog=cog, error=str(e)))

    # Comando: q!enable <cog>
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def enable(self, ctx: Context, cog: str = None):       
        settings = await get_guild_settings(ctx.guild.id)
        if cog is None:
            await ctx.send(get_message(settings["language"], "help_enable"))
            return
        if cog not in settings["enabled_cogs"]:
            settings["enabled_cogs"].append(cog)
            await update_guild_settings(ctx.guild.id, settings)
            await ctx.send(get_message(settings["language"], "enable_success", cog=cog))
        else:
            await ctx.send(get_message(settings["language"], "enable_already", cog=cog))

    # Comando: q!disable <cog>
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def disable(self, ctx: Context, cog: str = None):       
        settings = await get_guild_settings(ctx.guild.id)
        if cog is None:
            await ctx.send(get_message(settings["language"], "help_disable"))
            return
        if cog in settings["enabled_cogs"]:
            settings["enabled_cogs"].remove(cog)
            await update_guild_settings(ctx.guild.id, settings)
            await ctx.send(get_message(settings["language"], "disable_success", cog=cog))
        else:
            await ctx.send(get_message(settings["language"], "disable_already", cog=cog))

    # Comando: q!listextensions
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def listextensions(self, ctx: Context):
        settings = await get_guild_settings(ctx.guild.id)
        
        all_extensions = [f[:-3] for f in os.listdir("cogs") if f.endswith(".py")]
        
        loaded_extensions = list(self.bot.extensions.keys())
        
        formatted_extensions = []
        for ext in all_extensions:
            if f"cogs.{ext}" in loaded_extensions:
                formatted_extensions.append(f"__{ext}__")
            else:
                formatted_extensions.append(ext)
        
        prefix = "\n - "
        extensions_str = prefix + prefix.join(formatted_extensions)
        
        await ctx.send(get_message(settings["language"], "list_extensions", extensions=extensions_str))

    # Comando: q!loadall
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def loadall(self, ctx: Context):
        settings = await get_guild_settings(ctx.guild.id)
        extensions = [f[:-3] for f in os.listdir("cogs") if f.endswith(".py")]
        
        for cog in extensions:
            try:
                await self.bot.load_extension(f"cogs.{cog}")
                if cog not in settings["loaded_cogs"]:
                    settings["loaded_cogs"].append(cog)
            except Exception as e:
                await ctx.send(get_message(settings["language"], "load_all_error", error=str(e)))
                return
        
        await update_guild_settings(ctx.guild.id, settings)
        await ctx.send(get_message(settings["language"], "load_all_success"))

    # Comando: q!unloadall
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unloadall(self, ctx: Context):
        settings = await get_guild_settings(ctx.guild.id)
        
        for cog in settings["loaded_cogs"]:
            try:
                if cog == 'config':
                    continue
                await self.bot.unload_extension(f"cogs.{cog}")
            except Exception as e:
                await ctx.send(get_message(settings["language"], "unload_all_error", error=str(e)))
                return
        
        settings["loaded_cogs"] = []
        await update_guild_settings(ctx.guild.id, settings)
        await ctx.send(get_message(settings["language"], "unload_all_success"))
            
    # Comando: q!setlang <lang>
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setlang(self, ctx: Context, lang: str = None):
        settings = await get_guild_settings(ctx.guild.id)
        if cog is None:
            await ctx.send(get_message(settings["language"], "help_setlang"))
            return
        if lang not in ["en_us", "pt_br", "es"]:
            await ctx.send(get_message(settings["language"], "setlang_invalid", languages=", ".join(["en_us", "pt_br", "es"])))
            return

        settings["language"] = lang
        await update_guild_settings(ctx.guild.id, settings)
        await ctx.send(get_message(lang, "setlang_success", selected_language=lang))

    # Comando: q!lang
    @commands.command()
    async def lang(self, ctx: Context):
        settings = await get_guild_settings(ctx.guild.id)
        await ctx.send(get_message(settings["language"], "lang_current", selected_language=settings["language"]))

async def setup(bot):
    await bot.add_cog(Config(bot))