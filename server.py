import websockets
import asyncio
import os
import json

LOG_FILE_PATH = 'log.txt'
PORT = 8001
CHECK_INTERVAL = 2
NUM_INITIAL_LOGS = 10

async def read_last_n_lines(n, file_path=LOG_FILE_PATH):
    """Read the last N lines from the log file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        last_line = file_size
        block_size = 1024
        lines = []

        while len(lines) < n and file.tell() > 0:
            seek_position = min(file_size, file.tell() - block_size)
            file.seek(seek_position)
            block = file.read(block_size)
            lines.extend(block.splitlines())
            file_size -= block_size

        return lines[-n:], last_line

def get_last_line(file_path=LOG_FILE_PATH):
    """Get the position of the last line in the log file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        file.seek(0, os.SEEK_END)
        return file.tell()

async def send_logs_to_client(websocket, logs):
    """Send log entries to the connected client."""
    for message in logs:
        event = {"type": "new", "message": message}
        await websocket.send(json.dumps(event))

async def monitor_log_file(websocket):
    """Monitor the log file for changes and send updates to the client."""
    print("WebSocket connection established.")
    
    # Initial retrieval of last N logs
    logs, last_line = await read_last_n_lines(NUM_INITIAL_LOGS)
    print(f"Sending {len(logs)} initial log entries to the client.")
    await send_logs_to_client(websocket, logs)

    while True:
        current_last_line = get_last_line()

        if current_last_line > last_line:
            # New log entries found, send them to the client
            logs, last_line = await read_last_n_lines(1)
            print(f"New log entry found: {logs[0]}")
            await send_logs_to_client(websocket, logs)

        await asyncio.sleep(CHECK_INTERVAL)

async def handler(websocket, path):
    """WebSocket handler function."""
    await monitor_log_file(websocket)

async def main():
    """Main asynchronous function to start the WebSocket server."""
    async with websockets.serve(handler, "", PORT):
        print(f"WebSocket server started on port {PORT}.")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
