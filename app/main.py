import os
from fastapi import FastAPI
from openai import OpenAI

# Удаляем переменные прокси, которые могут мешать
os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)
os.environ.pop("http_proxy", None)
os.environ.pop("https_proxy", None)

app = FastAPI()

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
