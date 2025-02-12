import os

class Config:
    IMAGE_FOLDER = os.getenv("IMAGE_FOLDER", "assets")
    SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT = int(os.getenv("SERVER_PORT", 8080))
