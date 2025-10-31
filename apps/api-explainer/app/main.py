from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers import health, explain
from .middleware import request_id_middleware


app = FastAPI(title="SimpleDoc API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",")],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(health.router)
app.include_router(explain.router)

@app.middleware("http")
async def _request_id(request, call_next):
    return await request_id_middleware(request, call_next)


