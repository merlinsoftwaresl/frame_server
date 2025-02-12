import argparse
import asyncio
import websockets
from server.config import Config
from server.image_loader import load_images_from_folder
from server.handlers import handle_client

async def main():
    load_images_from_folder(args.folder)
    server = await websockets.serve(handle_client, Config.SERVER_HOST, Config.SERVER_PORT)
    print("Server started")
    await server.wait_closed()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WebSocket image server")
    parser.add_argument("--folder", type=str, default=Config.IMAGE_FOLDER, help="Path to the folder containing images")
    args = parser.parse_args()
    Config.IMAGE_FOLDER = args.folder

    asyncio.run(main())
