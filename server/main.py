import argparse
from fastapi import FastAPI
import uvicorn
from server.config import Config
from server.image_loader import load_images_from_folder
from server.handlers import setup_routes

app = FastAPI()

def main():
    # Load images
    load_images_from_folder(args.folder)
    
    # Setup routes
    setup_routes(app)
    
    # Start server
    uvicorn.run(app, host=Config.SERVER_HOST, port=Config.SERVER_PORT)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="REST image server")
    parser.add_argument("--folder", type=str, default=Config.IMAGE_FOLDER, help="Path to the folder containing images")
    args = parser.parse_args()
    Config.IMAGE_FOLDER = args.folder

    main()
