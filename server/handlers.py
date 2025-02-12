import asyncio
import websockets
import server.image_loader as img
from server.config import Config


async def send_image(websocket, image_data):
        try:
            await websocket.send(image_data)
            print("Image sent.")

            ack = await asyncio.wait_for(websocket.recv(), timeout=15)
            if ack == "ACK":
                print("Acknowledgment received from client.")
                if image_data in img.image_queue:
                    img.image_queue.popleft()
            else:
                print(f"Unexpected acknowledgment: {ack}")

        except asyncio.TimeoutError:
            print("No acknowledgment received. Retrying...")
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connection lost. Error: {e}")
            return

async def handle_client(websocket, path):
    while True:
        try:
            message = await websocket.recv()
            if message == "REQUEST_IMAGE":
                if not img.image_queue:
                    print("Image queue empty. Reloading...")
                    img.load_images_from_folder(Config.IMAGE_FOLDER)
                if img.image_queue:
                    await send_image(websocket, img.image_queue[0])
            elif message.startswith("REQUEST:"):
                filename = message.split(":", 1)[1]
                if filename in img.image_map:
                    await send_image(websocket, img.image_map[filename])
                else:
                    print(f"Requested image not found: {filename}")
                    await websocket.send("ERROR: Image not found")
        except websockets.exceptions.ConnectionClosedError:
            print("Connection lost. Waiting for client to reconnect...")
            break
