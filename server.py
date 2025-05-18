import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import httpx
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("OPENAI_API_KEY")

app.mount("/static", StaticFiles(directory="client"), name="static")


@app.get("/token")
async def get_token():
    """Return a session token from the OpenAI Realtime API."""
    if not API_KEY:
        raise HTTPException(status_code=500, detail="Missing OPENAI_API_KEY")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/realtime/sessions",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json",
                },
                json={"model": "gpt-4o-realtime-preview-2024-12-17", "voice": "verse"},
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to generate token") from e


@app.get("/{full_path:path}", response_class=HTMLResponse)
async def serve_frontend(full_path: str):
    """Serve the React frontend for any non-API route."""
    index_file = Path("client/index.html")
    if index_file.exists():
        return index_file.read_text(encoding="utf-8")
    raise HTTPException(status_code=404, detail="Index file not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 3000)))
