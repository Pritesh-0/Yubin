import asyncio
import sys

async def handle_client(reader, writer):

    async def read():
        while True:
            data = await reader.read(100)
            if not data:
                break

            message = data.decode()
            print(f"Received: {message}")
            sys.stdout.flush()

    async def write():
        while True:
            response = input("enter message: ")
            if response.lower() == 'exit':
                break

            writer.write(response.encode())
            await writer.drain()
            sys.stdout.flush()

            await asyncio.sleep(1)


    try:
        task_read = asyncio.create_task(read())
        task_write = asyncio.create_task(write())
        await asyncio.gather(task_read, task_write)
    finally:
        writer.close()

async def main():
    server = await asyncio.start_server(
        handle_client, '127.0.0.1', 8888
    )

    addr = server.sockets[0].getsockname()

    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())

