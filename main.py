__all__ = []

from logging.config import dictConfig

from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi_utils.tasks import repeat_every
from tortoise.contrib.fastapi import register_tortoise

from app import models
from app.controllers.broadcasts import broadcast
from app.routers import oauth, users, servers, servers_data, xbox, websocket
from app.settings import DATABASE_URL, MODELS_FILE, LOG_CONFIG

app = FastAPI()

app.include_router(oauth.router, prefix="/api/oauth", tags=["auth"])
app.include_router(xbox.router, prefix="/api/xbox", tags=["xbox"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(servers.router, prefix="/api/servers", tags=["servers"])
app.include_router(servers_data.router, prefix="/api/servers", tags=["servers"])
app.include_router(websocket.router, prefix="/api/websocket", tags=["ws"])

dictConfig(
    LOG_CONFIG
)

register_tortoise(
    app,
    db_url=DATABASE_URL,
    modules={"models": [MODELS_FILE]},
    generate_schemas=True
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)


@app.on_event("startup")
async def start_up():
    await broadcast.connect()

    await broadcast.create_channel("servers_info")
    async for server_obj in models.Server.all():
        channel = f"server_data:{server_obj.id}"
        await broadcast.create_channel(channel)


@app.on_event("startup")
@repeat_every(seconds=5)
async def publish_broadcast_queue():
    await broadcast.publish_queue()


@app.on_event("shutdown")
async def shutdown():
    await broadcast.disconnect()


@app.get("", response_class=FileResponse)
async def index():
    return FileResponse("C:/dev/2021/app_MAPP/dist/index.html")
