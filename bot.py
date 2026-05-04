import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

import os
TOKEN = os.environ.get("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

kelimeler = {
        'Palto':'Abrigo','Büyükanne':'Abuela','Büyükbaba':'Abuelo','Su':'Agua','Şimdi':'Ahora','Almanca':'Aleman','Almanya':'Alemania','Orada':'Alli','Daire':'Apartamento','Burda':'Aqui','Sanat':'Arte','Şeker':'Azucar','Banka':'Banco','Mahalle':'Barrio','İyi':'Bien','Hoş Geldin':'Bien Venida','Poşet':'Bolsa','Güzel':'Bonito','Günaydın':'Buenos Dias','Kahve':'Cafe','Kafe':'Cafeteria','Sıcak':'Calor','Şarj Cihazı':'Cargador','Cüzdan':'Cartera','Avm':'Centro Comercial','Yakınlarda':'Cerca','Güle Güle':'Chao','Ceket':'Chaqueta','Şehir':'Ciudad','Nasıl':'Como','Oda Arkadaşı':'Companero De Cuarto','Sanırım':'Creo Que','Ne Kadar':'Cuanto Cuesto','Aralık':'Diciembre','İki':'Dos','Şeftali':'Durazno','Bina':'Edifico','Genelde':'En General','Aslında':'En Realidad','Memnun Oldum':'Encantado','Ocak':'Enero','İspanyolca':'Espanol','Karı':'Esposa','Koca':'Esposo','Otopark':'Estacionamiento','Bu':'Este','Çalışmak':'Estudiar','Fransızca':'Frances','Fransa':'Francia','Soğuk':'Frio','Garaj':'Garaje','Şapka':'Gorra','Teşekkürler':'Gracias','Komik':'Graciosa','Büyük':'Grande','Vay':'Guau','Konuşmak':'Hablar','Hava':'Hace','Görüşürüz':'Hasta Luego','Dondurma':'Helado','Kız Kardeş':'Hermana','Erkek Kardeş':'Hermano','Buz':'Hielo','Kız':'Hija','Oğul':'Hijo','Otel':'Hotel','Bugün':'Hoy','İngilizce':'Ingles','İtalyanca':'Italiano','Kış':'Invierno','Bahçe':'Jardin','Meyve Suyu':'Jugo','Temmuz':'Julio','Süt':'Leche','Uzak':'Lejos','Kitabevi':'Libraria','Kitap':'Libro','Valiz':'Maleta','Sabah':'Manana','Mango':'Mango','Mart':'Marzo','En Büyük':'Mas Grande','En İyi':'Mejor','Pazar':'Mercado','Bak':'Mira','Çanta':'Mochila','Çok':'Mucho','Memnun Oldum':'Mucho Gusto','Müze':'Museo','Müzik':'Musica','Portakal':'Naranja','İhtiyaç Var':'Necesito','Hayır':'No','Değil Mi':'No Crees','Gece':'Noche','Kız Arkadaş':'Novia','Erkek Arkadaş':'Novio','Yeni':'Nuevo','Veya':'O','Ekim':'Octubre','Sonbahar':'Otono','Hey':'Oye','Ülke':'Pais','Ekmek':'Pan','Fırın':'Panaderia','Sevgili':'Pareja','Park':'Parque','Küçük':'Pequeno','Mükemmel':'Perfecto','Ama':'Pero','Ananas':'Pina','Kat':'Piso','Biraz':'Poco','Portekizce':'Portugues','İlkbahar':'Primavera','Kasaba':'Pueblo','Saat':'Reloj','Karpuz':'Sandia','Eylül':'Septiembre','Ciddi':'Serio','Evet':'Si','Sempatik':'Simpatico','Güneş':'Sol','Sadece':'Solamento','Yalnız':'Solo','Süveter':'Sueter','Tablet':'Tableto','"-Da"':'Tambien','Çay':'Te','Sahiplik':'Tengo','Teras':'Terraza','Teyze':'Tia','Mağaza':'Tienda','Utangaç':'Timido','Amca':'Tio','Mayo':'Traje De Bano','Sakin':'Tranquilo','Üç':'Tres','Giymek':'Usar','Yaz':'Verano','Değil Mi ?':'Verdad','Elbise':'Vestido','Rüzgarlı':'Viento','Yaşamak':'Vivir','Ve':'Y'
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