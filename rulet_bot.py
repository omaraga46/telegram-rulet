import logging
import random
import asyncio
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Logging ayarları
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Oyun Ayarları
BAŞLANGIÇ_BAKİYESİ = 1000
SABİT_BAHİS_MİKTARI = 10
SAYI_ÖDEME_ORANI = 36

# Renk tanımlamaları
RENKLER = {
    0: "🟢",  # Yeşil
    1: "🔴", 2: "⚫️", 3: "🔴", 4: "⚫️", 5: "🔴",
    6: "⚫️", 7: "🔴", 8: "⚫️", 9: "🔴", 10: "⚫️",
    11: "⚫️", 12: "🔴", 13: "⚫️", 14: "🔴", 15: "⚫️",
    16: "🔴", 17: "⚫️", 18: "🔴", 19: "🔴", 20: "⚫️",
    21: "🔴", 22: "⚫️", 23: "🔴", 24: "⚫️", 25: "🔴",
    26: "⚫️", 27: "🔴", 28: "⚫️", 29: "⚫️", 30: "🔴",
    31: "⚫️", 32: "🔴", 33: "⚫️", 34: "🔴", 35: "⚫️",
    36: "🔴"
}

# Kullanıcı verileri
kullanici_verileri = {}

def create_rulet_keyboard() -> InlineKeyboardMarkup:
    """Rulet için klavye oluşturur"""
    keyboard = []
    row = []
    for i in range(37):
        if i % 6 == 0 and row:
            keyboard.append(row)
            row = []
        row.append(InlineKeyboardButton(str(i), callback_data=f"rulet_{i}"))
    if row:
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Bot başlatıldığında çalışır"""
    user = update.effective_user
    user_id = user.id
    
    if user_id not in kullanici_verileri:
        kullanici_verileri[user_id] = {
            'bakiye': BAŞLANGIÇ_BAKİYESİ,
            'aktif_bahis': None
        }
    
    # Web App butonu oluştur
    keyboard = [[InlineKeyboardButton(
        "🎰 Rulet Oyununu Başlat",
        web_app=WebAppInfo(url="https://YOUR-GITHUB-USERNAME.github.io/telegram-rulet/rulet.html")  # GitHub Pages URL'si
    )]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"🎰 Rulet Oyununa Hoş Geldin {user.first_name}!\n\n"
        f"💰 Bakiye: {kullanici_verileri[user_id]['bakiye']}₺\n"
        f"🎲 Bahis: {SABİT_BAHİS_MİKTARI}₺\n\n"
        f"Oyunu başlatmak için aşağıdaki butona tıkla!",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Buton tıklamalarını işler"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    if user_id not in kullanici_verileri:
        await query.edit_message_text("Önce /start komutu ile oyunu başlatmalısın!")
        return
    
    data = query.data
    
    if data.startswith("rulet_"):
        # Sayı seçimi
        sayi = int(data.split("_")[1])
        kullanici_verileri[user_id]['aktif_bahis'] = {
            'tip': 'sayi',
            'deger': sayi,
            'miktar': SABİT_BAHİS_MİKTARI
        }
        await query.edit_message_text(
            f"✅ {sayi}{RENKLER[sayi]} numarasına {SABİT_BAHİS_MİKTARI}₺ bahis yaptın!\n"
            f"Çarkı çevirmek için '🔄 Çevir' butonuna tıkla.",
            reply_markup=create_rulet_keyboard()
        )
    
    elif data in ["renk_kirmizi", "renk_siyah", "tek", "cift"]:
        # Renk veya tek/çift bahsi
        kullanici_verileri[user_id]['aktif_bahis'] = {
            'tip': data,
            'miktar': SABİT_BAHİS_MİKTARI
        }
        bahis_tipi = {
            'renk_kirmizi': '🔴 Kırmızı',
            'renk_siyah': '⚫️ Siyah',
            'tek': '1️⃣ Tek',
            'cift': '2️⃣ Çift'
        }[data]
        await query.edit_message_text(
            f"✅ {bahis_tipi} seçeneğine {SABİT_BAHİS_MİKTARI}₺ bahis yaptın!\n"
            f"Çarkı çevirmek için '🔄 Çevir' butonuna tıkla.",
            reply_markup=create_rulet_keyboard()
        )
    
    elif data == "cevir":
        # Çarkı çevir
        if not kullanici_verileri[user_id]['aktif_bahis']:
            await query.edit_message_text("Önce bir bahis yapmalısın!", reply_markup=create_rulet_keyboard())
            return
        
        # Bakiye kontrolü
        if kullanici_verileri[user_id]['bakiye'] < SABİT_BAHİS_MİKTARI:
            await query.edit_message_text("Yetersiz bakiye!", reply_markup=create_rulet_keyboard())
            return
        
        # Bahsi al
        kullanici_verileri[user_id]['bakiye'] -= SABİT_BAHİS_MİKTARI
        
        # Animasyonlu dönüş efekti
        dönüş_mesajları = [
            "🎡 Çark dönüyor...",
            "🎡 Çark dönüyor... 🔄",
            "🎡 Çark dönüyor... 🔄 🔄",
            "🎡 Çark dönüyor... 🔄 🔄 🔄",
            "🎡 Çark dönüyor... 🔄 🔄 🔄 🔄",
            "🎡 Çark dönüyor... 🔄 🔄 🔄 🔄 🔄"
        ]
        
        for mesaj in dönüş_mesajları:
            await query.edit_message_text(mesaj, reply_markup=create_rulet_keyboard())
            await asyncio.sleep(0.5)  # 0.5 saniye bekle
        
        # Çarkı çevir
        kazanan_sayi = random.randint(0, 36)
        kazanan_renk = RENKLER[kazanan_sayi]
        
        # Top animasyonu
        top_konumlari = ["⬆️", "↗️", "➡️", "↘️", "⬇️", "↙️", "⬅️", "↖️"]
        for konum in top_konumlari:
            await query.edit_message_text(
                f"🎡 Çark dönüyor...\n"
                f"🎯 Top: {konum}",
                reply_markup=create_rulet_keyboard()
            )
            await asyncio.sleep(0.2)
        
        # Sonucu kontrol et
        bahis = kullanici_verileri[user_id]['aktif_bahis']
        kazanc = 0
        
        if bahis['tip'] == 'sayi' and bahis['deger'] == kazanan_sayi:
            kazanc = SABİT_BAHİS_MİKTARI * SAYI_ÖDEME_ORANI
        elif bahis['tip'] == 'renk_kirmizi' and kazanan_renk == "🔴":
            kazanc = SABİT_BAHİS_MİKTARI * 2
        elif bahis['tip'] == 'renk_siyah' and kazanan_renk == "⚫️":
            kazanc = SABİT_BAHİS_MİKTARI * 2
        elif bahis['tip'] == 'tek' and kazanan_sayi % 2 == 1:
            kazanc = SABİT_BAHİS_MİKTARI * 2
        elif bahis['tip'] == 'cift' and kazanan_sayi % 2 == 0 and kazanan_sayi != 0:
            kazanc = SABİT_BAHİS_MİKTARI * 2
        
        # Kazancı ekle
        kullanici_verileri[user_id]['bakiye'] += kazanc
        
        # Sonucu göster
        sonuc_mesaji = (
            f"🎲 Çark durdu!\n\n"
            f"🏆 Kazanan: {kazanan_sayi}{kazanan_renk}\n\n"
        )
        
        if kazanc > 0:
            sonuc_mesaji += f"🎉 Tebrikler! {kazanc}₺ kazandın!\n"
        else:
            sonuc_mesaji += "😕 Maalesef kazanamadın.\n"
        
        sonuc_mesaji += f"\n💰 Yeni Bakiye: {kullanici_verileri[user_id]['bakiye']}₺"
        
        # Bahsi sıfırla
        kullanici_verileri[user_id]['aktif_bahis'] = None
        
        await query.edit_message_text(sonuc_mesaji, reply_markup=create_rulet_keyboard())
    
    elif data == "iptal":
        # Bahsi iptal et
        kullanici_verileri[user_id]['aktif_bahis'] = None
        await query.edit_message_text(
            f"❌ Bahis iptal edildi.\n\n"
            f"💰 Bakiye: {kullanici_verileri[user_id]['bakiye']}₺",
            reply_markup=create_rulet_keyboard()
        )

def main() -> None:
    """Botu başlatır"""
    # Bot token'ını .env dosyasından al
    from dotenv import load_dotenv
    import os
    load_dotenv()
    
    application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()
    
    # Komut işleyicileri
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Botu başlat
    application.run_polling()

if __name__ == "__main__":
    main()