from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.handler import register_exception_handlers
from app.api.v1 import (
    auth,
    artists,
    users,
    albums,
    tracks,
    playlists,
    likes,
)
from app.api.v1.admin import (
    playlists as admin_playlists,
    analytics as admin_analytics,
)

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(artists.router)
app.include_router(albums.router)
app.include_router(tracks.router)
app.include_router(playlists.router)
app.include_router(likes.router)
app.include_router(admin_playlists.router)
app.include_router(admin_analytics.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

register_exception_handlers(app)

@app.get("/")
async def health_check():
    return {
        "message": "Welcome to Tunify backend!"
    }
