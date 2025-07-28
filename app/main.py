from fastapi import FastAPI, Request
from app.controller import guardar_en_excel
import uvicorn

app = FastAPI()


@app.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()

    if not payload.get("ref"):
        return {"status": "ignored"}

    head_commit = payload["head_commit"]
    name = head_commit["author"]["name"]
    email = head_commit["author"]["email"]
    username = head_commit["author"]["username"]
    timestamp = head_commit["timestamp"]
    message = head_commit["message"]
    url = head_commit["url"]
    repository_name = payload["repository"]["name"]

    print(f"Commit by {name} ({email}, {username}) at {timestamp}: {message}")

    guardar_en_excel(payload)

    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
