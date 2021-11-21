import asyncio
from websockets import connect


async def hello(uri):
    async with connect(uri) as websocket:
        await websocket.send("Hello world!")
        await websocket.recv()


asyncio.run(hello("ws://192.168.68.105:8000/ws"))
