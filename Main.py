import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
import os
from yt_dlp import YoutubeDL

# Bot bilgileri
API_ID = 27646440
API_HASH = "5a519873d92b53bfaa987a2953181f22"
BOT_TOKEN = "7996394881:AAHffuYmn43uS83VymaJRp2me7XUTE_D9sU"

# Pyrogram istemcisi
bot = Client("MusicBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
pytgcalls = PyTgCalls(bot)

# YouTube video indirme ayarları
def download_song(query):
    ydl_opts = {
        "format": "bestaudio/best",
        "extractaudio": True,
        "audioformat": "mp3",
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "noplaylist": True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=True)
        return info["title"], ydl.prepare_filename(info)

# Bot komutları
@bot.on_message(filters.command("oynat") & filters.private)
async def play_song(client: Client, message: Message):
    query = message.text.split(None, 1)[1]
    chat_id = message.chat.id

    # Şarkıyı indir
    await message.reply("Şarkı aranıyor ve indiriliyor...")
    try:
        title, filepath = download_song(query)
        await message.reply(f"Şarkı indirildi: {title}")

        # Sesli sohbete bağlan ve şarkıyı çal
        await pytgcalls.join_group_call(
            chat_id,
            AudioPiped(filepath)
        )
        await message.reply(f"Şarkı çalıyor: {title}")
    except Exception as e:
        await message.reply(f"Hata oluştu: {e}")

# Bot çalıştırma
async def main():
    await bot.start()
    await pytgcalls.start()
    print("Bot çalışıyor...")
    await asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    asyncio.run(main())
