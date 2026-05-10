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
    türkçe, ispanyolca = random.choice(list(kelimeler.items()))
    aktif_sorular[chat_id] = {
        'türkçe': türkçe,
        'ispanyolca': ispanyolca,
        'yanlis': 0,
        'acik': 0,
        'mod': mod  # 'tr_isp' veya 'isp_tr'
    }
    return türkçe, ispanyolca

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Hola! İspanyolca kelime botuna hoş geldin!\n\n"
        "📚 Komutlar:\n"
        "/sor — Türkçe → İspanyolca sorar\n"
        "/sor_tr_isp — İspanyolca → Türkçe sorar\n"
        "/ogret kelime:cevap — Yeni kelime ekle\n"
        "/liste — Tüm kelimeleri gör\n"
        "kelime anlamı — Kelimenin İspanyolcasını öğren\n\n"
        "💡 Yanlış cevaplarda ipucu harfleri açılır, 3 yanlışta cevap gösterilir!"
    )

@dp.message(Command("sor"))
async def sor(message: types.Message):
    if not kelimeler:
        await message.answer("Kelime listesi boş! /ogret ile kelime ekle.")
        return
    türkçe, ispanyolca = yeni_soru_baslat(message.chat.id, 'tr_isp')
    ipucu_bos = ipucu_goster(ispanyolca, 0)
    await message.answer(f"🇪🇸 '{türkçe}' kelimesinin İspanyolcası nedir?\n\n{ipucu_bos}")

@dp.message(Command("sor_tr_isp"))
async def sor_tr_isp(message: types.Message):
    if not kelimeler:
        await message.answer("Kelime listesi boş! /ogret ile kelime ekle.")
        return
    türkçe, ispanyolca = yeni_soru_baslat(message.chat.id, 'isp_tr')
    ipucu_bos = ipucu_goster(türkçe, 0)
    await message.answer(f"🇹🇷 '{ispanyolca}' kelimesinin Türkçesi nedir?\n\n{ipucu_bos}")

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
    metin = message.text.strip()

    # "kelime anlamı" özelliği
    if metin.lower().endswith(" anlamı") or metin.lower().endswith(" anlami"):
        aranan = metin.lower().replace(" anlamı", "").replace(" anlami", "").strip().title()
        if aranan in kelimeler:
            await message.answer(f"📖 '{aranan}' = 🇪🇸 {kelimeler[aranan]}")
        else:
            await message.answer(f"❓ '{aranan}' kelimesi listede bulunamadı.")
        return

    if chat_id not in aktif_sorular:
        return

    soru = aktif_sorular[chat_id]
    türkçe = soru['türkçe']
    ispanyolca = soru['ispanyolca']
    mod = soru['mod']
    verilen = metin.lower()

    # Moda göre soru ve cevap belirle
    if mod == 'tr_isp':
        soru_kelime = türkçe
        dogru = ispanyolca
        yeni_mod_flag = 'tr_isp'
        soru_oku = lambda t, i: f"➡️ Sıradaki soru:\n🇪🇸 '{t}' kelimesinin İspanyolcası nedir?\n\n"
        soru_oku2 = lambda t, i: f"➡️ 🇪🇸 '{t}' kelimesinin İspanyolcası nedir?\n\n"
        ipucu_kelime = lambda t, i: i
    else:
        soru_kelime = ispanyolca
        dogru = tür