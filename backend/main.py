import os
import asyncio
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

# Telegram bot (aiogram)
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, WebAppData
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.types.input_file import FSInputFile
import json

# === Load ENV ===
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# === Bot setup ===
bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

@dp.message(F.text == "/start")
async def start(message: Message):
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📨 Kirim Menfess", web_app=WebAppInfo(url="https://anonmenfess-bot-production.up.railway.app"))]  # Ganti URL di sini
    ], resize_keyboard=True)
    await message.answer("Selamat datang! Klik tombol di bawah untuk kirim menfess:", reply_markup=kb)

@dp.message(F.web_app_data)
async def handle_webapp_data(message: Message):
    try:
        data = json.loads(message.web_app_data.data)
        text = data.get("message", "")
        tags = data.get("tags", "")
        print(data)
        media_path = data.get("media_path")
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

# === Lifespan untuk menjalankan bot saat FastAPI start ===
@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(dp.start_polling(bot))
    yield
    await bot.session.close()

app = FastAPI(lifespan=lifespan)

# === Serve frontend ===
frontend_dir = Path(__file__).parent.parent / "frontend"
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="static")

# === Form endpoint ===
@app.post("/submit")
async def submit_form(
    message: str = Form(...),
    tags: str = Form(...),
    media: UploadFile = None
):
    print("📨 Menfess diterima!")
    media_path = None

    if media:
        media_dir = Path("media")
        media_dir.mkdir(exist_ok=True)
        media_path = media_dir / media.filename
        with open(media_path, "wb") as f:
            f.write(await media.read())

    print("p")
    return {
        "message": message,
        "tags": tags,
        "media_path": str(media_path) if media else None
    }

# === Untuk local run ===
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
