from fastapi import FastAPI, Request
from app.controllers.controller import guardar_en_excel
import uvicorn

app = FastAPI()


@app.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()

    try:
        # Procesar el payload y guardar los datos en Excel
        guardar_en_excel(payload)

    except Exception as e:
        print(f"Error al procesar el webhook: {e}")
        return {"status": "error"}

    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
