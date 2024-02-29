import websockets
import asyncio

import json
import time

Messages = [
    "Hey",
    "Thank God We did it",
    "Let's take to next level"
]


async def handler(websocket):
    # "Read file"
    # create event
    for message in Messages:
        print(f"sending msg: {message}...")
        event = {
                "type": "new",
                "message": message,
            }
        await websocket.send(json.dumps(event))
        await asyncio.sleep(2)
    # async for message in websocket:
    #     print(message)
    #     event = {
    #             "type": "new",
    #             "message": "Are you ready?",
    #         }
    #     await websocket.send(json.dumps(event))


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
