Start websocat server 
first download the  websockets.asyncio.server import serve
make sure to creat a venv for python to run 
then istall the websocat library 
make sure it's working by this command " python -m pip show websockets "
test the server by trying " python -c "from websockets.asyncio.server import serve; print('Success!')" " 


## WebSockets Library: Built-in vs. Custom Functionality

| Functionality | Available in the Library? |
|---|---|
| Create a WebSocket server using `serve()` | ✅ Built-in |
| Connect to a WebSocket server using `connect()` | ✅ Built-in |
| Send messages using `send()` | ✅ Built-in |
| Receive messages using `recv()` | ✅ Built-in |
| Handle multiple concurrent connections | ✅ Supported |
| Echo Server — Send the same message back to the client | ✍️ Custom implementation |
| Chat Server — Send messages to other connected users | ✍️ Custom implementation |
| Game Server — Handle player movements and calculate scores | ✍️ Custom implementation |
| Notification Server — Decide when and to whom notifications are sent | ✍️ Custom implementation |

**Note:** The `websockets` library provides the communication tools, while developers implement the application-specific logic based on their project's requirements.
v