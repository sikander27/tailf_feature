import websockets
import asyncio

async def handle_client(websocket, path):
    # This function is called for each WebSocket connection
    print(f"Client connected: {websocket.remote_address}")

    try:
        while True:
            message = await websocket.recv()  # Wait for incoming message
            print(f"Received message from {websocket.remote_address}: {message}")

            # Echo the received message back to the client
            await websocket.send(f"Echo: {message}")
    except websockets.exceptions.ConnectionClosedError:
        print(f"Client disconnected: {websocket.remote_address}")

async def main():
    async with websockets.serve(handle_client, "localhost", 8000):
        print("WebSocket server started on port 8000.")
        await asyncio.Future()  # Keep the server running

if __name__ == "__main__":
    asyncio.run(main())

