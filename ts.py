import asyncio

async def handle_client(reader, writer):
    address = writer.get_extra_info('peername')
    print(f"Accepted connection from {address}")

    async def receive():
        while True:
            data = await reader.read(100)
            if not data:
                break

            message = data.decode()
            print(f"Received from {address}: {message}")

    async def send():
        while True:
            try:
                response = await asyncio.to_thread(input, "enter message: ")
            except asyncio.CancelledError:
                break
            writer.write(response.encode())
            await writer.drain()

    receiver = asyncio.create_task(receive())
    sender = asyncio.create_task(send())

    await asyncio.gather(receiver, sender, return_exceptions=True)

    writer.close()

async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8888)

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
        asyncio.run(main())

