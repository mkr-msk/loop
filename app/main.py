from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import activities, sessions, users

app = FastAPI(title="Loop API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(activities.router)
app.include_router(sessions.router)
app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "Loop API is running"}