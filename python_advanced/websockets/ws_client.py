#!/usr/bin/env python3

"""A simple asynchronous WebSocket client."""

import asyncio
import websockets


async def connect_and_send(uri: str, text: str) -> str:
    """Connect to a WebSocket server and send a message."""
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello WebSocket")
        response = await websocket.recv()
        return response


async def main():
    """Run the WebSocket client."""
    response = await connect_and_send(
        "ws://localhost:8765", "demo"
    )
    print(response, end="")


if __name__ == "__main__":
    asyncio.run(main())
