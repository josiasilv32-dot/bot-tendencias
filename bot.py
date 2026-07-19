import os, json, requests, random
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
DATA_FILE = "tendencias_cache.json"

def get_crypto_trends():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/search/trending", timeout=8)
        data = r.json()
        coins = data.get('coins',[])[:7]
        out = []
        for c in coins:
            item = c.get('item',{})
            out.append(f"{item.get('symbol','')} ({item.get('name','')})")
        return out
    except:
        return ["BTC - Bitcoin","ETH - Ethereum","SOL - Solana"]

def get_global_news_trends():
    base_world = [
        "Copa do Mundo 2026 - Eliminatorias",
        "Bitcoin / BTC",
        "IA / ChatGPT / Grok",
        "Euro / Futebol Europa",
        "MrBeast / Viral",
        "GTA 6",
        "Eleicoes EUA",
        "Netflix Top 1",
        "TikTok Viral"
    ]
    base_pt = [
        "Benfica / Porto / Sporting",
        "IRS / Financas Portugal",
        "Casas / Alojamento",
        "Lidl / Pingo Doce",
        "Praia / Algarve / Faro",
        "Emprego / Salario Minimo",
        "Liga Portugal",
        "Bitcoin Portugal"
    ]
    return base_world, base_pt

def analise_atencao():
    hora = datetime.now().hour
    if 6 <= hora < 12:
        momento = "Manha: Pessoas em NOTICIAS, BOLSA, TRABALHO"
    elif 12 <= hora < 18:
        momento = "Tarde: FUTEBOL, MEMES, COMPRAS"
    else:
        momento = "Noite: ATENCAO MAXIMA em ENTRETENIMENTO - Filmes, Futebol, Streams"
    
    return f"""
🧠 ONDE ESTA A ATENCAO AGORA ({datetime.now().strftime('%H:%M')} Lisbon)

{momento}

1. CONSUMO (90%): Vendo final, TikTok, Netflix -> COMPRAM dopamina
2. OPORTUNIDADE (9%): Pesquisando Bitcoin, casas, emprego -> QUEREM mudar
3. DOMINACAO (1% - TU): Correndo domingo 21h, criando bot

💡 Pega o #1 do momento (Futebol Final) + teu nicho = "passeio de domingo conta como treino?"
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 BOT TENDENCIAS ON\n/tendencias - Mundo+PT\n/pt - Portugal\n/mundo - Mundo\n/crypto - Crypto\n/atencao - Onde esta a atencao\n/acao - O que fazem agora")

async def tendencias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mundo, pt = get_global_news_trends()
    crypto = get_crypto_trends()
    texto = f"🌍 TENDENCIAS {datetime.now().strftime('%d/%m %H:%M')}\n\n🇵🇹 PT TOP 5:\n"
    for i, t in enumerate(random.sample(pt, 5), 1):
        texto += f"{i}. {t}\n"
    texto += "\n🌎 MUNDO TOP 5:\n"
    for i, t in enumerate(random.sample(mundo, 5), 1):
        texto += f"{i}. {t}\n"
    texto += "\n₿ CRYPTO:\n"
    for i, c in enumerate(crypto[:5], 1):
        texto += f"{i}. {c}\n"
    await update.message.reply_text(texto)

async def cmd_pt(update, context):
    _, pt = get_global_news_trends()
    await update.message.reply_text("🇵🇹 PORTUGAL:\n" + "\n".join([f"{i}. {t}" for i, t in enumerate(pt, 1)]))

async def cmd_mundo(update, context):
    mundo, _ = get_global_news_trends()
    await update.message.reply_text("🌎 MUNDO:\n" + "\n".join([f"{i}. {t}" for i, t in enumerate(mundo, 1)]))

async def cmd_crypto(update, context):
    crypto = get_crypto_trends()
    await update.message.reply_text("₿ CRYPTO TRENDING:\n" + "\n".join([f"{i}. {c}" for i, c in enumerate(crypto, 1)]))

async def cmd_atencao(update, context):
    await update.message.reply_text(analise_atencao())

async def cmd_acao(update, context):
    await update.message.reply_text("🎯 ACAO AGORA:\n🔍 Pesquisando: final, bitcoin, emprego\n🛒 Comprando: cerveja, apostas\n👀 Assistindo: final, Netflix, TikTok\n💸 TU: produz enquanto consomem")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tendencias", tendencias))
    app.add_handler(CommandHandler("t", tendencias))
    app.add_handler(CommandHandler("pt", cmd_pt))
    app.add_handler(CommandHandler("portugal", cmd_pt))
    app.add_handler(CommandHandler("mundo", cmd_mundo))
    app.add_handler(CommandHandler("crypto", cmd_crypto))
    app.add_handler(CommandHandler("atencao", cmd_atencao))
    app.add_handler(CommandHandler("acao", cmd_acao))
    print("BOT RODANDO...")
    app.run_polling()

if __name__ == "__main__":
    main()
