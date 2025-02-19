import os
import base64
from collections import deque

image_queue = deque()
image_map = {}

def load_images_from_folder(folder_path):
    if not os.path.exists(folder_path):
        print(f"Assets folder not found: {folder_path}")
        return
    
    # Clear existing queues
    image_queue.clear()
    image_map.clear()
    
    for filename in sorted(os.listdir(folder_path)):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, "rb") as image_file:
                file_extension = os.path.splitext(filename)[1][1:].lower()
                encoded_image = f"data:image/{file_extension};base64,{base64.b64encode(image_file.read()).decode()}"
                image_queue.append(encoded_image)
                image_map[filename] = encoded_image
                print(f"Image enqueued: {filename}")
