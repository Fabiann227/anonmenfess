from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, WebAppData
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.types.input_file import FSInputFile
import asyncio
import json
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]

bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

@dp.message(F.text == "/start")
async def start(message: Message):
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📨 Kirim Menfess", web_app=WebAppInfo(url="https://8ce3-66-96-225-172.ngrok-free.app"))]
    ], resize_keyboard=True)
    await message.answer("Selamat datang! Klik tombol di bawah untuk kirim menfess:", reply_markup=kb)

@dp.message(F.web_app_data)
async def handle_webapp_data(message: Message):
    try:
        data = json.loads(message.web_app_data.data)
        text = data.get("message", "")
        tags = data.get("tags", "")
        media_path = data.get("media_path")

        print(media_path)
        caption = f"<b>📢 Menfess Anonim</b>\n\n{text}\n\n{tags}"

        if media_path and os.path.exists(media_path):
            input_file = FSInputFile(media_path)
            if media_path.lower().endswith((".mp4", ".mov")):
                await bot.send_video(CHANNEL_ID, input_file, caption=caption)
            else:
                await bot.send_photo(CHANNEL_ID, input_file, caption=caption)
        else:
            await bot.send_message(CHANNEL_ID, caption)

        await message.answer("✅ Menfess berhasil dikirim.")
    except Exception as e:
        print("WebApp Data Error:", e)
        await message.answer("❌ Gagal mengirim menfess.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
