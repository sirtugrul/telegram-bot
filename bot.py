import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

import os
TOKEN = os.environ.get("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

kelimeler = {
    'sevgili':'Pareja','yalnız':'Solo','kat':'Piso','küçük':'Pequeno','uzak':'Lejos','daire':'Apartamento','yaşamak':'Vivo','bina':'Edifico',' en büyük':'Mas grande','bu':'Este','üç':'Tres','mango':'Mango','iki':'Dos','portakal':'Naranja','ne kadar':'Cuanto cuesto','şeftali':'Durazno','ihtiyaç':'Necesito','Pazar':'Mercado','poşet':'Bolsa','ananas':'Pina','karpuz':'Sandia','aralık':'Diciembre','ekim':'Octubre','orada':'Alli','çok':'Mucho','güneş':'Sol','kış':'İnvierno','ilkbahar':'Primavera','eylül':'Septiembre','ülke':'Pais','mart':'Marzo','bugün':'Hoy','mayo':'Traje de bano','yaz':'Verano','şimdi':'Ahora','temmuz':'Julio','ocak':'Enero','sıcak':'Calor','rüzgarlı':'Viento','hava':'Hace','giymek':'Uso','palto':'Abrigo','sonbahar':'Otono','soğuk':'Frio','sanat':'Arte','müzik':'Musica','çalışmak':'Estudias','gece':'Noche','sabah':'Manana','vay':'Guau','almanca':'Aleman','italyanca':'İtaliano','biraz':'Poco','konuşmak':'Hablo',' fransızca':'Frances ','ingilizce':'Ingles','ispanyolca':'Espanol','Portekizce':'Portugues','kasaba':'Pueblo','bak':'Mira','park':'Parque','şehir':'Ciudad','hey':'Oye','otel':'Hotel','kitabevi':'Libraria','mahalle':'Barrio','otopark':'Estacionamiento','banka':'Banço','AVM':'Centro comercial','yakınlarda':'Cerca','müze':'Museo','kafe':'Cafeteria','fırın':'Panaderia','mağaza':'Tienda','çanta':'Mochila','tablet':'Tableto',' kitap':'Libro','yeni':'Nuevo','şarj cihazı':'Cargador','şapka':'Gorra','saat':'Reloj','süveter':'Sueter','ceket':'Chaqueta','elbise':'Vestido','cüzdan':'Cartera','burda':'Aqui','sakin':'Tranquilo','valiz':'Maleta','ciddi':'Serio','komik':'Graciosa ','nasıl':'Como','ama':'Pero ','erkek arkadaş':'Novio',' kız arkadaş':'Novia ','genelde':'En general','sanırım':'Creo que',' sempatik':'Simpitico','değil mi':'No crees',' utangaç':'Timido','büyükanne':'Abuela','büyükbaba':'Abuelo','karı':'Esposa ','koca':'Esposo','sadece':'Solamento',' -da':'Tambien','teyze':'Tia','amca':'Tio',' aslında':'En realidad','kız':'Hija ','oğul':'Hijo','var':'Tengo','kız kardeş':'hermana','erkek kardeş':'hermano',' oda arkadaşı':'Companero de cuarto','Hayır':'No',' evet':'Si','değil mi ?':'Verdad ','Fransa':'Francia','Almanya':'Alemania','meyve suyu':'Jugo','iyi':'Bien','memnun oldum':'Encantado','hoş geldin':'Bien venida','en iyi':'Mejor','günaydın':'Buenos dias','memnun oldum':'Mucho gusto','görüşürüz':'Hasta luego','ekmek':'Pan','dondurma':'Helado','şeker':'Azucar','mükemmel':'Perfecto','teşekkürler':'Gracias','güle güle':'Chao','ve':'Y','su':'Agua','buz':'Hielo','veya':'O','çay':'Te',' kahve':'Cafe','süt':'Leche'

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