import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from openai import OpenAI

app = FastAPI()

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
def root():
    return {"message": "PostPilot AI is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/generate-post")
def generate_post(business: str, niche: str):
    prompt = f"Напиши пост для соцсетей для бизнеса '{business}' в нише 
'{niche}'. Пост полезный, вовлекающий, 150-200 слов."
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"post": response.choices[0].message.content}
