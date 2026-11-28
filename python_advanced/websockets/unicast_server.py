#!/usr/bin/env python3
"""Unicast WebSocket server: replies only to the sender with 'U:' prefix."""
import asyncio

import websockets

connected_clients = set()


async def connection_handler(websocket):
    """Track the client and answer each message only to its sender."""
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            await websocket.send("U:" + message)
    except websockets.ConnectionClosed:
        pass
    finally:
        connected_clients.discard(websocket)


async def main():
    """Start the server on 127.0.0.1:8765 and run forever."""
    async with websockets.serve(connection_handler, "127.0.0.1", 8765):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
