mkdir -p ~/adptvbot
cat > ~/adptvbot/bot.py << 'EOF'
import telebot
from telebot import types

# Ganti dengan token bot kamu
TOKEN = "8448482018:AAGMj5JrKCkg2fIhjb-D_DR0P-2RggKwczw"
bot = telebot.TeleBot(TOKEN)

# ===== START COMMAND =====
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("👤 ADMIN", "🔗 URL PLAYLIST", "📦 PAKET PLAYLIST")
    bot.send_message(
        message.chat.id,
        "🤖 Selamat datang di *ADP TV BOT*\n\nSilakan lakukan pilihan anda 👇",
        parse_mode="Markdown",
        reply_markup=markup
    )

# ===== HANDLER MENU =====
@bot.message_handler(func=lambda msg: True)
def menu_handler(message):
    text = message.text

    # === ADMIN ===
    if text == "👤 ADMIN":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("💬 Hubungi Admin", url="https://t.me/alvasr123"))
        markup.add(types.InlineKeyboardButton("📱 WhatsApp Admin", url="https://wa.me/628123456789"))
        bot.send_message(message.chat.id, "📌 Klik tombol di bawah untuk hubungi admin 👇", reply_markup=markup)

    # === URL PLAYLIST ===
    elif text == "🔗 URL PLAYLIST":
        bot.send_message(message.chat.id, "🔗 Playlist Free IPTV:\nhttps://adptv.short.gy/playlist")

    # === PAKET PLAYLIST ===
    elif text == "📦 PAKET PLAYLIST":
        paket_info = """**Paket IPTV ADP TV Premium**

- Paket Bulanan:
  • 1 Bulan: Rp 16.000
  • 3 Bulan: Rp 45.000
  • 6 Bulan: Rp 75.000
  • 12 Bulan: Rp 110.000

✨ Keuntungan Premium:
- Akses ribuan channel TV premium
- Streaming stabil & jernih
- Support HP, Tablet, Smart TV
- Navigasi mudah

Pilih paket yang sesuai 👇
"""
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("💎 PREMIUM", callback_data="premium"))
        bot.send_message(message.chat.id, paket_info, parse_mode="Markdown", reply_markup=markup)

# ===== CALLBACK HANDLER =====
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    data = call.data

    # === PREMIUM ===
    if data == "premium":
        text = """Varian: Paket Premium  
Silakan pilih paket Type yang akan di-deploy:"""
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("PREMIUM", callback_data="premium_list"))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

    # === LIST PREMIUM ===
    elif data == "premium_list":
        text = """== **PILIH PAKET (ADP TV • PREMIUM )** ==

[ 1 ] 1 BULAN  
[ 3 ] 3 BULAN  
[ 6 ] 6 BULAN  
[ 12 ] 12 BULAN  

♻️ Silakan pilih angka spek yang ingin anda deploy."""
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("1 Bulan", callback_data="paket_1"),
            types.InlineKeyboardButton("3 Bulan", callback_data="paket_3"),
        )
        markup.add(
            types.InlineKeyboardButton("6 Bulan", callback_data="paket_6"),
            types.InlineKeyboardButton("12 Bulan", callback_data="paket_12"),
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    # === DETAIL PAKET ===
    elif data.startswith("paket_"):
        paket = data.split("_")[1]
        harga_map = {
            "1": "16 Rb Per Bulan",
            "3": "45 Rb / 3 Bulan",
            "6": "75 Rb / 6 Bulan",
            "12": "110 Rb / 12 Bulan"
        }
        harga = harga_map[paket]

        text = f"""────🌐 **PLAYLIST 🌐────
💠 **FITUR**  
🔅 LIVE → EVENT PREMIUM  
📺 TV LOKAL  
⚽ SPORTS  
🎬 MOVIES  
🎞 SERIAL  
📽 FILM 2025  

💰 Harga: {harga}
────────────────────────"""

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("💳 Bayar Paket", callback_data=f"bayar_{paket}"))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    # === BAYAR (dengan QRIS berbeda) ===
    elif data.startswith("bayar_"):
        paket = data.split("_")[1]
        harga_map = {
            "1": "Rp 16.000",
            "3": "Rp 45.000",
            "6": "Rp 75.000",
            "12": "Rp 110.000"
        }
        qr_map = {
            "1": "qris_1.png",
            "3": "qris_3.png",
            "6": "qris_6.png",
            "12": "qris_12.png"
        }

        harga = harga_map[paket]
        qris_file = qr_map[paket]

        text = f"""💳 *PEMBAYARAN PAKET PREMIUM*  

Nominal: {harga}  
Admin Fee: Rp 0  
Total Bayar: {harga}  
⏰ Timeout: 5 menit  

📱 Scan QR ini & bayar Total Bayar."""
        try:
            with open(qris_file, "rb") as qr:
                bot.send_photo(call.message.chat.id, qr, caption=text, parse_mode="Markdown")
        except:
            bot.send_message(call.message.chat.id, f"⚠️ QRIS {paket} bulan belum tersedia.")

        # Tambahkan tombol cek pembayaran
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔃 Cek Pembayaran", url="https://wa.me/62895810355575"))
        bot.send_message(call.message.chat.id, "Klik tombol di bawah untuk konfirmasi pembayaran 👇", reply_markup=markup)


print("🤖 Bot sedang berjalan...")
bot.infinity_polling()
EOF







