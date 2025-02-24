import os
import discord
from discord.ext import commands
from discord.ext.commands import Context
from database.guild_settings import get_guild_settings
from utils.locales import get_message
from deepl import Translator
from dotenv import load_dotenv
from utils.secrets import get_secret

# Carregar variáveis do arquivo .env
load_dotenv()

SECRET_ID = os.getenv("GOOGLE_CLOUD_SECRET_ID_DEEPL")

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.translator = Translator(get_secret(SECRET_ID))

    @commands.command()
    async def translate(self, ctx: Context, target_lang: str, *, text: str):
        """
        Traduz uma mensagem para o idioma especificado.
        Uso: q!translate <idioma_alvo> <texto>
        Exemplo: q!translate pt_br Hello, how are you?
        """
        settings = await get_guild_settings(ctx.guild.id)
        
        lang_map = {
            "en_us": "EN-US",  # Inglês (EUA)
            "pt_br": "PT-BR",  # Português (Brasil)
            "es": "ES"        # Espanhol
        }
        
        if target_lang not in lang_map:
            await ctx.send(get_message(settings["language"], "translate_invalid_lang", languages=", ".join(lang_map.keys())))
            return
        
        try:
            result = self.translator.translate_text(text, target_lang=lang_map[target_lang])
            await ctx.send(get_message(target_lang, "translate_success", target_lang=get_message(target_lang, 'language'), text=result.text))
        except Exception as e:
            await ctx.send(get_message(settings["language"], "translate_error", error=str(e)))

async def setup(bot):
    await bot.add_cog(Misc(bot))