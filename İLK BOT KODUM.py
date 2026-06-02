from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


from bist100 import BIST100

import yfinance as yf

from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
from ta.trend import MACD
from ta.trend import ADXIndicator


from telegram import ReplyKeyboardMarkup


from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator, MACD

import yfinance as yf
from ta.momentum import RSIIndicator

import yfinance as yf

from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
from ta.trend import MACD
from telegram.ext import MessageHandler, filters

TOKEN = "8885993910:AAE647ujVJ6pDLOn4Fa0lnmqX8PRc0AlYek"
CHAT_ID = 1140952929

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        ["📊 Tara"],
        ["✈️ THYAO"]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    await update.message.reply_text(
        "🚀 BIST Sinyal Botuna Hoş Geldin!",
        reply_markup=reply_markup
    )


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text == "📊 Tara":
        await tara(update, context)

    elif text == "✈️ THYAO":
        await thyao(update, context)




async def thyao(update: Update, context: ContextTypes.DEFAULT_TYPE):

    veri = yf.download(
        "THYAO.IS",
        period="6mo",
        progress=False
    )

    close = veri["Close"].squeeze()
    high = veri["High"].squeeze()
    low = veri["Low"].squeeze()
    volume = veri["Volume"].squeeze()

    fiyat = float(close.iloc[-1])

    rsi = RSIIndicator(
        close,
        window=14
    ).rsi().iloc[-1]

    ema20 = EMAIndicator(
        close,
        window=20
    ).ema_indicator().iloc[-1]

    ema50 = EMAIndicator(
        close,
        window=50
    ).ema_indicator().iloc[-1]

    macd = MACD(close)

    macd_line = macd.macd().iloc[-1]
    signal_line = macd.macd_signal().iloc[-1]

    adx = ADXIndicator(
        high=high,
        low=low,
        close=close,
        window=14
    )

    adx_deger = adx.adx().iloc[-1]

    ortalama_hacim = volume.tail(20).mean()
    son_hacim = volume.iloc[-1]

    puan = 0

    # RSI
    if rsi < 30:
        puan += 20
    elif rsi < 50:
        puan += 10

    # EMA20
    if fiyat > ema20:
        puan += 20

    # EMA50
    if fiyat > ema50:
        puan += 20

    # MACD
    if macd_line > signal_line:
        puan += 20

    # ADX
    if adx_deger > 25:
        puan += 10

    # HACİM
    if son_hacim > ortalama_hacim:
        puan += 10

    if puan >= 80:
        sinyal = "🚀 GÜÇLÜ AL"
    elif puan >= 60:
        sinyal = "🟢 AL"
    elif puan >= 40:
        sinyal = "🟡 NÖTR"
    else:
        sinyal = "🔴 SAT"

    mesaj = f"""
📈 THYAO

Fiyat: {fiyat:.2f}

RSI: {rsi:.2f}
EMA20: {ema20:.2f}
EMA50: {ema50:.2f}
ADX: {adx_deger:.2f}

Hacim: {int(son_hacim):,}

Puan: {puan}/100

{sinyal}
"""

    await update.message.reply_text(mesaj)

    await update.message.reply_text(mesaj)

    await update.message.reply_text(mesaj)


async def tara(update: Update, context: ContextTypes.DEFAULT_TYPE):

    hisseler = BIST100

    sonuclar = []

    for hisse in hisseler:
        ...


        try:

            veri = yf.download(
                hisse,
                period="6mo",
                progress=False
            )
            if veri.empty:
                print(f"{hisse} veri bulunamadı")
                continue
                
            close = veri["Close"].squeeze()
            high = veri["High"].squeeze()
            low = veri["Low"].squeeze()
            volume = veri["Volume"].squeeze()

            fiyat = float(close.iloc[-1])

            rsi = RSIIndicator(
                close,
                window=14
            ).rsi().iloc[-1]

            ema20 = EMAIndicator(
                close,
                window=20
            ).ema_indicator().iloc[-1]

            ema50 = EMAIndicator(
                close,
                window=50
            ).ema_indicator().iloc[-1]

            macd = MACD(close)

            macd_line = macd.macd().iloc[-1]
            signal_line = macd.macd_signal().iloc[-1]

            adx = ADXIndicator(
                high=high,
                low=low,
                close=close,
                window=14
            )

            adx_deger = adx.adx().iloc[-1]

            ortalama_hacim = volume.tail(20).mean()
            son_hacim = volume.iloc[-1]

            puan = 0

            # RSI
            if rsi < 30:
                puan += 20
            elif rsi < 50:
                puan += 10

            # EMA20
            if fiyat > ema20:
                puan += 20

            # EMA50
            if fiyat > ema50:
                puan += 20

            # MACD
            if macd_line > signal_line:
                puan += 20

            # ADX
            if adx_deger > 25:
                puan += 10

            # HACİM
            if son_hacim > ortalama_hacim:
                puan += 10

            sonuclar.append(
                (
                    hisse.replace(".IS", ""),
                    puan,
                    fiyat
                )
            )

        except Exception as e:
            print(e)

    sonuclar.sort(
        key=lambda x: x[1],
        reverse=True
    )

    mesaj = "📊 BIST TARAMA\n\n"

    for kod, puan, fiyat in sonuclar:

        if puan >= 80:
            emoji = "🚀"
        elif puan >= 60:
            emoji = "🟢"
        elif puan >= 40:
            emoji = "🟡"
        else:
            emoji = "🔴"

        mesaj += (
            f"{emoji} {kod}\n"
            f"Fiyat: {fiyat:.2f}\n"
            f"Puan: {puan}/100\n\n"
        )

    await update.message.reply_text(mesaj)



def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tara", tara))
    app.add_handler(CommandHandler("thyao", thyao))

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, menu)
    )

    print("Bot çalışıyor...")

    app.run_polling()

if __name__ == "__main__":
    main()