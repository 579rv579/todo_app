from contextlib import asynccontextmanager

from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import init_db

import requests as req

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print('DB initialized     bot ready')
    yield


app = FastAPI(title='my to do APP', lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

@app.get("api/tasks/{tg_id}")
async def tasks(tg_id: int):
    user = await req.add_user(tg_id)
    return await req.get_tasks(user.id)

@app.get("api/main/{tg_id}")
async def profile(tg_id: int):
    user = await req.add_user(tg_id)
    completed_tasks_count = await req.get_completed_tasks(user.id)
    return {'completed_tasks': completed_tasks_count} 