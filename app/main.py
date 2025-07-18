from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

@app.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()
    if payload.get("ref"):
        repo = payload["repository"]["full_name"]
        commits = payload.get("commits", [])
        print(f"\n🚀 Push en {repo}:")
        for commit in commits:
            print(f"- Autor: {commit['author']['name']}")
            print(f"  Mensaje: {commit['message']}")
            print(f"  URL: {commit['url']}")
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
