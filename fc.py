import asyncio
import websockets

class TestWebsocketsClient:
    def __init__(self):
        asyncio.run(self.main())
    
    async def main(self):
        async with websockets.connect("ws://127.0.0.1:8765") as websocket:
            while True:
                async for message in websocket:
                    print(f"Received: {message}")
                    client_msg = f"Message from client-{message.split('-')[-1]}"
                    await asyncio.sleep(2)
                    print(f"Sending: {client_msg}")
                    print(f"--")
                    await websocket.send(client_msg)

if __name__ == '__main__':
    websocketsClient = TestWebsocketsClient()

