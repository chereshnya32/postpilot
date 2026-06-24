import os
import httpx
from fastapi import FastAPI
from openai import OpenAI

app = FastAPI()

# Создаём HTTP клиент без прокси (игнорируем системные переменные HTTP_PROXY/HTTPS_PROXY)
http_client = httpx.Client(
    proxies=None,  # явно отключаем прокси
    follow_redirects=True,
)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.proxyapi.ru/openai/v1",
    http_client=http_client,  # передаём клиент без прокси
)

@app.get("/")
def root():
    return {"message": "PostPilot AI is running (via ProxyAPI)"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/generate-post")
def generate_post(business: str, niche: str):
    prompt = f"Напиши пост для соцсетей для бизнеса '{business}' в нише '{niche}'. Пост полезный, вовлекающий, 150-200 слов."
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"post": response.choices[0].message.content}
