import websockets
import asyncio

import os
import json


def read_last_n_lines(n, file_path='log.txt'):
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
        print(len(lines))
        return lines[-n:], last_line


def get_last_line(file_path='log.txt'):
    with open(file_path, 'r', encoding='utf-8') as file:
        file.seek(0, os.SEEK_END)
        last_line = file.tell()

        return last_line


async def handler(websocket):
    logs, last_line = read_last_n_lines(10)
    print(f"Last line is {last_line}")
    for message in logs:
        event = {
                "type": "new",
                "message": message,
            }
        await websocket.send(json.dumps(event))
    while True:
        if get_last_line() > last_line:
            logs, last_line = read_last_n_lines(1)
            for message in logs:
                print(message)
                event = {
                        "type": "new",
                        "message": message,
                    }
                await websocket.send(json.dumps(event))
        await asyncio.sleep(2)


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())


