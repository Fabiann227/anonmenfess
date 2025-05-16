from fastapi import FastAPI, UploadFile, Form, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

frontend_dir = Path(__file__).parent.parent / "frontend"

# Mount static files di /static supaya gak konflik dengan API
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/")
async def root():
    # Kirim index.html saat akses root
    return FileResponse(frontend_dir / "index.html")

@app.get("/{file_path:path}")
async def serve_file(file_path: str):
    # Kirim file statis lain (css, js, dll) dari frontend folder
    target = frontend_dir / file_path
    if target.exists() and target.is_file():
        return FileResponse(target)
    return FileResponse(frontend_dir / "index.html")

@app.post("/submit")
async def submit_form(
    message: str = Form(...),
    tags: str = Form(...),
    media: UploadFile = None
):
    print("📨 Menfess diterima!")
    media_path = None

    if media:
        media_dir = Path(__file__).parent / "uploads"
        media_dir.mkdir(exist_ok=True)
        media_path = media_dir / media.filename
        with open(media_path, "wb") as f:
            f.write(await media.read())

    return {
        "message": message,
        "tags": tags,
        "media_path": str(media_path) if media else None
    }
