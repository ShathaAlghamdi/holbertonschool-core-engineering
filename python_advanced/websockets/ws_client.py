#!/usr/bin/env python3

"""Echo server using the asyncio API."""

import asyncio
import websockets
from websockets.asyncio.server import serve


async def connect_and_send(uri: str ,text:str) -> str:
    """Connect to a websocket server and send a message."""
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello WebSocket")
        response = await websocket.recv()
        return response

async def main():
    response = await connect_and_send("ws://127.0.0.1:8765", "demo")
    print(response, end="")

if __name__ == "__main__":
    asyncio.run(main())
