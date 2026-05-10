# -*- coding: utf-8 -*-
import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import os

TOKEN = os.environ.get("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

kelimeler = {
    'Palto':'Abrigo','Buyukanne':'Abuela','Buyukbaba':'Abuelo','Su':'Agua',
    'Simdi':'Ahora','Almanca':'Aleman','Almanya':'Alemania','Orada':'Alli',
    'Daire':'Apartamento','Burda':'Aqui','Sanat':'Arte','Seker':'Azucar',
    'Banka':'Banco','Mahalle':'Barrio','Iyi':'Bien','Hos Geldin':'Bien Venida',
    'Poset':'Bolsa','Guzel':'Bonito','Gunaydin':'Buenos Dias','Kahve':'Cafe',
    'Kafe':'Cafeteria','Sicak':'Calor','Sarj Cihazi':'Cargador','Cuzdan':'Cartera',
    'Avm':'Centro Comercial','Yakinlarda':'Cerca','Gule Gule':'Chao','Ceket':'Chaqueta',
    'Sehir':'Ciudad','Nasil':'Como','Oda Arkadasi':'Companero De Cuarto',
    'Sanirim':'Creo Que','Ne Kadar':'Cuanto Cuesto','Aralik':'Diciembre','Iki':'Dos',
    'Seftali':'Durazno','Bina':'Edifico','Genelde':'En General','Aslinda':'En Realidad',
    'Memnun Oldum':'Encantado','Ocak':'Enero','Ispanyolca':'Espanol','Kari':'Esposa',
    'Koca':'Esposo','Otopark':'Estacionamiento','Bu':'Este','Calismak':'Estudiar',
    'Fransizca':'Frances','Fransa':'Francia','Soguk':'Frio','Garaj':'Garaje',
    'Sapka':'Gorra','Tesekkurler':'Gracias','Komik':'Graciosa','Buyuk':'Grande',
    'Vay':'Guau','Konusmak':'Hablar','Hava':'Hace','Gorusuruz':'Hasta Luego',
    'Dondurma':'Helado','Kiz Kardes':'Hermana','Erkek Kardes':'Hermano','Buz':'Hielo',
    'Kiz':'Hija','Ogul':'Hijo','Otel':'Hotel','Bugun':'Hoy','Ingilizce':'Ingles',
    'Italyanca':'Italiano','Kis':'Invierno','Bahce':'Jardin','Meyve Suyu':'Jugo',
    'Temmuz':'Julio','Sut':'Leche','Uzak':'Lejos','Kitabevi':'Libraria','Kitap':'Libro',
    'Valiz':'Maleta','Sabah':'Manana','Mango':'Mango','Mart':'Marzo',
    'En Buyuk':'Mas Grande','En Iyi':'Mejor','Pazar':'Mercado','Bak':'Mira',
    'Canta':'Mochila','Cok':'Mucho','Muze':'Museo','Muzik':'Musica',
    'Portakal':'Naranja','Ihtiyac Var':'Necesito','Hayir':'No','Gece':'Noche',
    'Kiz Arkadas':'Novia','Erkek Arkadas':'Novio','Yeni':'Nuevo','Veya':'O',
    'Ekim':'Octubre','Sonbahar':'Otono','Hey':'Oye','Ulke':'Pais','Ekmek':'Pan',
    'Firin':'Panaderia','Sevgili':'Pareja','Park':'Parque','Kucuk':'Pequeno',
    'Mukemmel':'Perfecto','Ama':'Pero','Ananas':'Pina','Kat':'Piso','Biraz':'Poco',
    'Portekizce':'Portugues','Ilkbahar':'Primavera','Kasaba':'Pueblo','Saat':'Reloj',
    'Karpuz':'Sandia','Eylul':'Septiembre','Ciddi':'Serio','Evet':'Si',
    'Sempatik':'Simpatico','Gunes':'Sol','Sadece':'Solamente','Yalniz':'Solo',
    'Suveter':'Sueter','Tablet':'Tableta','Cay':'Te','Teras':'Terraza',
    'Teyze':'Tia','Magaza':'Tienda','Utangac':'Timido','Amca':'Tio',
    'Mayo':'Traje De Bano','Sakin':'Tranquilo','Uc':'Tres','Giymek':'Usar',
    'Yaz':'Verano','Elbise':'Vestido','Ruzgarli':'Viento','Yasamak':'Vivir','Ve':'Y'
}

aktif_sorular = {}

def ipucu_goster(cevap: str, acik_harf: int) -> str:
    sonuc = ""
    harf_sayaci = 0
    for karakter in cevap:
        if karakter == " ":
            sonuc += " "
        else:
            if harf_sayaci < acik_harf:
                sonuc += karakter
                harf_sayaci += 1
            else:
                sonuc += "_"
    return sonuc

def yeni_soru_baslat(chat_id: int, mod: str):
    turkce, ispanyolca = random.choice(list(kelimeler.items()))
    aktif_sorular[chat_id] = {
        'turkce': turkce,
        'ispanyolca': ispanyolca,
        'yanlis': 0,
        'acik': 0,
        'mod': mod
    }
    return turkce, ispanyolca

@dp.message(Command("start"))
async def start(message: types.Message):
    aktif_sorular.pop(message.chat.id, None)
    await message.answer(
        "Hola! Ispanyolca kelime botuna hos geldin!\n\n"
        "Komutlar:\n"
        "/sor_turToisp - Turkce sorar, Ispanyolca cevap\n"
        "/sor_ispTotur - Ispanyolca sorar, Turkce cevap\n"
        "/ogret kelime:cevap - Yeni kelime ekle\n"
        "/liste - Tum kelimeleri gor\n"
        "kelime anlami - Kelimenin Ispanyolcasini gor\n\n"
        "Yanlis cevaplarda ipucu harfleri acilir, 3 yanliста cevap gosterilir!"
    )

@dp.message(Command("sor_turToisp"))
async def sor(message: types.Message):
    aktif_sorular.pop(message.chat.id, None)
    if not kelimeler:
        await message.answer("Kelime listesi bos!")
        return
    turkce, ispanyolca = yeni_soru_baslat(message.chat.id, 'tr_isp')
    ipucu_bos = ipucu_goster(ispanyolca, 0)
    await message.answer(f"'{turkce}' kelimesinin Ispanyolcasi nedir?\n\n{ipucu_bos}")

@dp.message(Command("sor_ispTotur"))
async def sor2(message: types.Message):
    aktif_sorular.pop(message.chat.id, None)
    if not kelimeler:
        await message.answer("Kelime listesi bos!")
        return
    turkce, ispanyolca = yeni_soru_baslat(message.chat.id, 'isp_tr')
    ipucu_bos = ipucu_goster(turkce, 0)
    await message.answer(f"'{ispanyolca}' kelimesinin Turkcesi nedir?\n\n{ipucu_bos}")

@dp.message(Command("ogret"))
async def ogret(message: types.Message):
    aktif_sorular.pop(message.chat.id, None)
    try:
        metin = message.text.split(" ", 1)[1]
        turkce, ispanyolca = metin.split(":")
        kelimeler[turkce.strip()] = ispanyolca.strip()
        await message.answer(f"'{turkce.strip()}' = '{ispanyolca.strip()}' eklendi!")
    except:
        await message.answer("Format: /ogret kelime:cevap\nOrnek: /ogret masa:mesa")

@dp.message(Command("liste"))
async def liste(message: types.Message):
    aktif_sorular.pop(message.chat.id, None)
    if not kelimeler:
        await message.answer("Liste bos.")
        return
    metin = "Kelime Listesi:\n\n"
    for tr, es in kelimeler.items():
        metin += f"{tr} = {es}\n"
    await message.answer(metin)

@dp.message()
async def cevap_kontrol(message: types.Message):
    chat_id = message.chat.id
    metin = message.text.strip()

    if metin.lower().endswith(" anlami"):
        aktif_sorular.pop(chat_id, None)
        aranan = metin.lower().replace(" anlami", "").strip().title()
        if aranan in kelimeler:
            await message.answer(f"'{aranan}' = {kelimeler[aranan]}")
        else:
            await message.answer(f"'{aranan}' kelimesi listede bulunamadi.")
        return

    if chat_id not in aktif_sorular:
        return

    soru = aktif_sorular[chat_id]
    turkce = soru['turkce']
    ispanyolca = soru['ispanyolca']
    mod = soru['mod']
    verilen = metin.lower()

    if mod == 'tr_isp':
        dogru = ispanyolca
        goster = turkce
        ipucu_kaynak = ispanyolca
        def sonraki(t, i):
            return f"Siradaki:\n'{t}' kelimesinin Ispanyolcasi nedir?\n\n{ipucu_goster(i, 0)}"
    else:
        dogru = turkce
        goster = ispanyolca
        ipucu_kaynak = turkce
        def sonraki(t, i):
            return f"Siradaki:\n'{i}' kelimesinin Turkcesi nedir?\n\n{ipucu_goster(t, 0)}"

    if verilen == dogru.lower():
        await message.answer(f"Dogru! '{goster}' = '{dogru}'")
        yeni_tr, yeni_isp = yeni_soru_baslat(chat_id, mod)
        await message.answer(sonraki(yeni_tr, yeni_isp))
    else:
        soru['yanlis'] += 1
        soru['acik'] += 1
        yanlis = soru['yanlis']

        if yanlis >= 3:
            await message.answer(f"3 yanlis! Cevap: '{dogru}'\n\nYeni soru geliyor...")
            yeni_tr, yeni_isp = yeni_soru_baslat(chat_id, mod)
            await message.answer(sonraki(yeni_tr, yeni_isp))
        else:
            ipucu = ipucu_goster(ipucu_kaynak, soru['acik'])
            await message.answer(f"Yanlis! ({yanlis}/3)\n\nIpucu: {ipucu}")

async def main():
    print("Bot calisiyor...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())