import discord
from discord.ext import commands
from discord.ext.commands import Context
from database.guild_settings import get_guild_settings
from utils.locales import get_message

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: Context):
        settings = await get_guild_settings(ctx.guild.id)
        await ctx.send(get_message(settings["language"], "ping_response"))

async def setup(bot):
    await bot.add_cog(Fun(bot))