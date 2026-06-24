import os
from fastapi import FastAPI
from openai import OpenAI

# Принудительно отключаем все прокси
os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""

app = FastAPI()

# Инициализация клиента (без дополнительных параметров)
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.proxyapi.ru/openai/v1"
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
