import artist.views
import audio.views
import collection.views
from database import database
from fastapi import FastAPI

app: FastAPI = FastAPI()

app.include_router(router=artist.views.router, prefix="/api/v1")
app.include_router(router=collection.views.router, prefix="/api/v1")
app.include_router(router=audio.views.router, prefix="/api/v1")


@app.on_event("startup")
async def on_startup():
    await database.connect()


@app.on_event("shutdown")
async def on_shutdown():
    await database.disconnect()
