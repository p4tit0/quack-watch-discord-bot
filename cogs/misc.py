import discord
from discord.ext import commands
from discord.ext.commands import Context
from database.guild_settings import get_guild_settings
from utils.locales import get_message

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def translate(self, ctx: Context):
        pass

async def setup(bot):
    await bot.add_cog(Fun(bot))