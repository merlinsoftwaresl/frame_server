from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
import base64
import server.image_loader as img
from server.config import Config

def setup_routes(app: FastAPI):
    @app.get("/images/next")
    async def get_next_image():
        """Get the next image in the queue"""
        if not img.image_queue:
            print("Image queue empty. Reloading...")
            img.load_images_from_folder(Config.IMAGE_FOLDER)
        
        if not img.image_queue:
            raise HTTPException(status_code=404, detail="No images available")
        
        image_data = img.image_queue.popleft()
        # Put it back at the end of the queue
        img.image_queue.append(image_data)
        
        # Extract the base64 data and content type
        content_type = image_data.split(';')[0].split(':')[1]
        base64_data = image_data.split(',')[1]
        
        # Decode base64 to binary
        binary_data = base64.b64decode(base64_data)
        
        return Response(content=binary_data, media_type=content_type)

    @app.get("/images/{filename}")
    async def get_image(filename: str):
        """Get a specific image by filename"""
        if filename not in img.image_map:
            raise HTTPException(status_code=404, detail="Image not found")
        
        image_data = img.image_map[filename]
        
        # Extract the base64 data and content type
        content_type = image_data.split(';')[0].split(':')[1]
        base64_data = image_data.split(',')[1]
        
        # Decode base64 to binary
        binary_data = base64.b64decode(base64_data)
        
        return Response(content=binary_data, media_type=content_type)
