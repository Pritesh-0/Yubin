import asyncio
import multiprocessing as mp
from websockets.server import serve
from websockets.exceptions import ConnectionClosedOK
import time

class DuplexWebsocketsServerProcess(mp.Process):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._send_queue = mp.Queue()

    def run(self):
        asyncio.run(self.main())

    def send(self, item):
        self._send_queue.put(item)

    async def consumer_handler(self, websocket):
        async for message in websocket:
            print(f"Received: {message}")
            print(f"--")

    async def producer_handler(self, websocket):
        while True:
            message = await asyncio.get_event_loop().run_in_executor(None, self._send_queue.get)
            print(f"Sending: {message}")
            try:
                await websocket.send(message)
            except ConnectionClosedOK:
                print("Connection closed..")
                break

    async def handler(self, websocket):
        await asyncio.gather(
            self.consumer_handler(websocket),
            self.producer_handler(websocket)
        )

    async def main(self):
        async with serve(self.handler, "0.0.0.0", 8765) as server:
            await asyncio.Future()

if __name__ == '__main__':
    socket_process = DuplexWebsocketsServerProcess(daemon=True)
    socket_process.start()

    time.sleep(2)
    for i in range(10):
        socket_process.send(f"Message from server-{i}")
        print(f"--\n")
        time.sleep(4)

    socket_process.join()
