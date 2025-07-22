import os
import uuid
from fastapi import UploadFile
from typing import Optional

VIDEO_DIR = os.getenv("VIDEO_STORAGE_DIR", "videos")


def save_video_file(file: UploadFile) -> str:
    if not os.path.exists(VIDEO_DIR):
        os.makedirs(VIDEO_DIR)

    video_id = str(uuid.uuid4())
    extension = os.path.splitext(file.filename)[1]
    filename = f"{video_id}{extension}"
    file_path = os.path.join(VIDEO_DIR, filename)

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    return video_id


def get_video_path_by_id(video_id: str) -> Optional[str]:
    if not os.path.exists(VIDEO_DIR):
        return None

    # Match files starting with the video_id
    for filename in os.listdir(VIDEO_DIR):
        if filename.startswith(video_id):
            return os.path.join(VIDEO_DIR, filename)
    return None
