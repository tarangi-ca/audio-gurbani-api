from banis.router import router as banis_router
from fastapi import FastAPI

app: FastAPI = FastAPI()
app.include_router(banis_router, prefix="/api/v1")
