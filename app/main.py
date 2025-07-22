import os
import uuid
import logging
from fastapi import FastAPI, File, UploadFile, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from app.storage import save_video_file, get_video_path_by_id
import yaml

# Load token from config
CONFIG_PATH = os.getenv("CONFIG_PATH", "application-local.yml")

try:
    with open(CONFIG_PATH, "r") as config_file:
        config = yaml.safe_load(config_file)
        AUTH_TOKEN = config.get("video-storage", {}).get("secret-token")
except Exception as e:
    raise RuntimeError(f"Failed to load config: {e}")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

origins = [
    "http://localhost:9000",
    "http://localhost:8080",
    "http://localhost:8081"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],   # You can restrict to ["GET", "POST"] if needed
    allow_headers=["*"],   # Or specify ["Authorization", "Content-Type"]
)


@app.post("/api/videos/upload")
async def upload_video(file: UploadFile = File(...), authorization: str = Header(None)):
    if not AUTH_TOKEN or authorization != AUTH_TOKEN:
        logger.warning("Unauthorized access attempt.")
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid or missing token.")

    try:
        video_id = save_video_file(file)
        logger.info(f"Video uploaded successfully: {video_id}")
        return {"videoId": video_id}
    except Exception as e:
        logger.exception("Failed to upload video")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/api/videos/{video_id}")
async def get_video(video_id: str):
    video_path = get_video_path_by_id(video_id)

    if not video_path or not os.path.exists(video_path):
        logger.warning(f"Requested video not found: {video_id}")
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Video not found")

    logger.info(f"Serving video: {video_id}")
    return FileResponse(video_path, media_type="video/mp4")

print("✅ Registered routes:")
for route in app.routes:
    print(f"{route.path} -> {route.name}")
