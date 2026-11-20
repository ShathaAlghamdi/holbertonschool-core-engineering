
#!/usr/bin/env python3

"""WebSocket server with message validation."""

import asyncio
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed


async def validate_message(websocket):
    """Validate incoming messages and send a response."""
    try:
        async for message in websocket:
            if len(message.strip()) == 0:
                await websocket.send("ERR:EMPTY")
            else:
                await websocket.send(f"OK:{message}")
    except ConnectionClosed:
        pass


async def main():
    """Start the WebSocket validation server."""
    async with serve(validate_message, "localhost", 8765):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
