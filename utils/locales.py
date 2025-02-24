import json

with open("locales.json", "r", encoding="utf-8") as f:
    LOCALES = json.load(f)

def get_message(lang, key, **kwargs):
    """
    Obtém uma mensagem traduzida com base no idioma e na chave fornecida.
    Substitui placeholders (ex: {lang}) pelos valores fornecidos.
    """
    if lang not in LOCALES:
        lang = "en_us"
    return LOCALES.get(lang, {}).get(key, "Message not found").format(**kwargs)