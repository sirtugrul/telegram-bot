import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = "8764241778:AAE4TuvYqrOCriOxUymdXd1a-IkS6x9Tygs"

bot = Bot(token=TOKEN)
dp = Dispatcher()

kelimeler = {
    "elma": "manzana",
    "ev": "casa",
    "araba": "coche",
    "kitap": "libro",
    "su": "agua",
    "güneş": "sol",
    "köpek": "perro",
    "kedi": "gato",
    "okul": "escuela",
    "arkadaş": "amigo",
}

aktif_sorular = {}

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Hola! İspanyolca kelime botuna hoş geldin!\n\n"
        "📚 Komutlar:\n"
        "/sor — Sana bir kelime sorayım\n"
        "/ogret kelime:cevap — Yeni kelime ekle\n"
        "/liste — Tüm kelimeleri gör"
    )

@dp.message(Command("sor"))
async def sor(message: types.Message):
    if not kelimeler:
        await message.answer("Kelime listesi boş! /ogret ile kelime ekle.")
        return
    türkçe, ispanyolca = random.choice(list(kelimeler.items()))
    aktif_sorular[message.chat.id] = (türkçe, ispanyolca)
    await message.answer(f"🇪🇸 '{türkçe}' kelimesinin İspanyolcası nedir?")

@dp.message(Command("ogret"))
async def ogret(message: types.Message):
    try:
        metin = message.text.split(" ", 1)[1]
        türkçe, ispanyolca = metin.split(":")
        kelimeler[türkçe.strip()] = ispanyolca.strip()
        await message.answer(f"✅ '{türkçe.strip()}' = '{ispanyolca.strip()}' eklendi!")
    except:
        await message.answer("⚠️ Format: /ogret kelime:cevap\nÖrnek: /ogret masa:mesa")

@dp.message(Command("liste"))
async def liste(message: types.Message):
    if not kelimeler:
        await message.answer("Liste boş.")
        return
    metin = "📖 Kelime Listesi:\n\n"
    for tr, es in kelimeler.items():
        metin += f"🇹🇷 {tr} → 🇪🇸 {es}\n"
    await message.answer(metin)

@dp.message()
async def cevap_kontrol(message: types.Message):
    chat_id = message.chat.id
    if chat_id not in aktif_sorular:
        return
    türkçe, doğru = aktif_sorular[chat_id]
    verilen = message.text.strip().lower()
    if verilen == doğru.lower():
        await message.answer(f"✅ Doğru! '{türkçe}' = '{doğru}' 🎉")
        del aktif_sorular[chat_id]
    else:
        await message.answer(f"❌ Yanlış! Tekrar dene.")

async def main():
    print("Bot çalışıyor... 🚀")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())