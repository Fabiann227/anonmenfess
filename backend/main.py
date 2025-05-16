import asyncio
from fastapi import FastAPI, Form, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from bot import setup_bot

app = FastAPI()

# Serve static frontend
frontend_dir = Path(__file__).parent.parent / "frontend"
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="static")

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

    return {
        "message": message,
        "tags": tags,
        "media_path": str(media_path) if media else None
    }

# Jalankan FastAPI + bot bersamaan
def start():
    import uvicorn
    loop = asyncio.get_event_loop()
    loop.create_task(setup_bot())  # jalanin bot
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    start()
