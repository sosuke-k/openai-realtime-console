import os
import json
import asyncio
import httpx
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

async def main():
    if not API_KEY:
        print(json.dumps({"error": "Missing OPENAI_API_KEY"}))
        return
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://api.openai.com/v1/realtime/sessions",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json",
                },
                json={"model": "gpt-4o-realtime-preview-2024-12-17", "voice": "verse"},
            )
            resp.raise_for_status()
            print(resp.text)
    except Exception:
        print(json.dumps({"error": "Failed to generate token"}))

if __name__ == "__main__":
    asyncio.run(main())
