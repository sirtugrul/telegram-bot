import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

import os
TOKEN = os.environ.get("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

kelimeler = {
    'Abrigo':'Palto','Abuela':'Büyükanne','Abuelo':'Büyükbaba','Agua':'Su','Ahora':'Şimdi','Aleman':'Almanca','Alemania':'Almanya','Alli':'Orada','Apartamento':'Daire','Aqui':'Burda','Arte':'Sanat','Azucar':'Şeker','Banco':'Banka','Barrio':'Mahalle','Bien':'İyi','Bien Venida':'Hoş Geldin','Bolsa':'Poşet','Bonito':'Güzel','Buenos Dias':'Günaydın','Cafe':'Kahve','Cafeteria':'Kafe','Calor':'Sıcak','Cargador':'Şarj Cihazı','Cartera':'Cüzdan','Centro Comercial':'Avm','Cerca':'Yakınlarda','Chao':'Güle Güle','Chaqueta':'Ceket','Ciudad':'Şehir','Como':'Nasıl','Companero De Cuarto':'Oda Arkadaşı','Creo Que':'Sanırım','Cuanto Cuesto':'Ne Kadar','Diciembre':'Aralık','Dos':'İki','Durazno':'Şeftali','Edifico':'Bina','En General':'Genelde','En Realidad':'Aslında','Encantado':'Memnun Oldum','Enero':'Ocak','Espanol':'İspanyolca','Esposa':'Karı','Esposo':'Koca','Estacionamiento':'Otopark','Este':'Bu','Estudiar':'Çalışmak','Frances':'Fransızca','Francia':'Fransa','Frio':'Soğuk','Garaje':'Garaj','Gorra':'Şapka','Gracias':'Teşekkürler','Graciosa':'Komik','Grande':'Büyük','Guau':'Vay','Hablar':'Konuşmak','Hace':'Hava','Hasta Luego':'Görüşürüz','Helado':'Dondurma','Hermana':'Kız Kardeş','Hermano':'Erkek Kardeş','Hielo':'Buz','Hija':'Kız','Hijo':'Oğul','Hotel':'Otel','Hoy':'Bugün','Ingles':'İngilizce','Italiano':'İtalyanca','Invierno':'Kış','Jardin':'Bahçe','Jugo':'Meyve Suyu','Julio':'Temmuz','Leche':'Süt','Lejos':'Uzak','Libraria':'Kitabevi','Libro':'Kitap','Maleta':'Valiz','Manana':'Sabah','Mango':'Mango','Marzo':'Mart','Mas Grande':'En Büyük','Mejor':'En İyi','Mercado':'Pazar','Mira':'Bak','Mochila':'Çanta','Mucho':'Çok','Mucho Gusto':'Memnun Oldum','Museo':'Müze','Musica':'Müzik','Naranja':'Portakal','Necesito':'İhtiyaç Var','No':'Hayır','No Crees':'Değil Mi','Noche':'Gece','Novia':'Kız Arkadaş','Novio':'Erkek Arkadaş','Nuevo':'Yeni','O':'Veya','Octubre':'Ekim','Otono':'Sonbahar','Oye':'Hey','Pais':'Ülke','Pan':'Ekmek','Panaderia':'Fırın','Pareja':'Sevgili','Parque':'Park','Pequeno':'Küçük','Perfecto':'Mükemmel','Pero':'Ama','Pina':'Ananas','Piso':'Kat','Poco':'Biraz','Portugues':'Portekizce','Primavera':'İlkbahar','Pueblo':'Kasaba','Reloj':'Saat','Sandia':'Karpuz','Septiembre':'Eylül','Serio':'Ciddi','Si':'Evet','Simpatico':'Sempatik','Sol':'Güneş','Solamento':'Sadece','Solo':'Yalnız','Sueter':'Süveter','Tableto':'Tablet','Tambien':'"-Da"','Te':'Çay','Tengo':'Sahiplik','Terraza':'Teras','Tia':'Teyze','Tienda':'Mağaza','Timido':'Utangaç','Tio':'Amca','Traje De Bano':'Mayo','Tranquilo':'Sakin','Tres':'Üç','Usar':'Giymek','Verano':'Yaz','Verdad':'Değil Mi ?','Vestido':'Elbise','Viento':'Rüzgarlı','Vivir':'Yaşamak','Y':'Ve'


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