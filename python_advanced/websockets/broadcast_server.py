#!/usr/bin/env python3
"""Broadcast WebSocket server: sends every message to all clients."""
import asyncio

import websockets

connected_clients = set()


async def connection_handler(websocket):
    """Track the client and broadcast each message with 'B:' prefix."""
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            websockets.broadcast(connected_clients, "B:" + message)
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
