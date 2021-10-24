import asyncio
import websockets
from PIL import Image
import json
import cv2
import numpy as np
import base64
from io import BytesIO
from controller import calculate_control_signal

async def echo(websocket, path):
    async for message in websocket:
        # Nhận hình ảnh từ giả lập
        data = json.loads(message)
        image = Image.open(BytesIO(base64.b64decode(data["image"])))
        image = np.asarray(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Tính toán góc lái và tốc độ
        # Ở phần này ta chưa sử dụng kết quả trả về
        throttle, steering_angle = calculate_control_signal(image)

async def main():
    async with websockets.serve(echo, "0.0.0.0", 4567, ping_interval=None):
        await asyncio.Future()  # run forever

asyncio.run(main())