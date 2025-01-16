import admin.views
import artist.views
import audio.views
import collection.views
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utilities.database import database

app: FastAPI = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router=artist.views.router, prefix="/api/v1")
app.include_router(router=collection.views.router, prefix="/api/v1")
app.include_router(router=audio.views.router, prefix="/api/v1")
app.include_router(router=admin.views.router, prefix="/api/v1")


@app.on_event("startup")
async def on_startup():
    await database.connect()


@app.on_event("shutdown")
async def on_shutdown():
    await database.disconnect()
