import os
from fastapi import FastAPI
from openai import OpenAI

app = FastAPI()

# Инициализация клиента с использованием ProxyAPI
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),  # Ваш ключ от ProxyAPI
    base_url="https://api.proxyapi.ru/openai/v1"  # Адрес ProxyAPI
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
        model="gpt-4o-mini",  # Можно заменить на "gpt-4" или другую модель, доступную в ProxyAPI
        messages=[{"role": "user", "content": prompt}]
    )
    return {"post": response.choices[0].message.content}
