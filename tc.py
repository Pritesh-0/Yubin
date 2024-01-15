import asyncio

async def receive(reader):
    while True:
        data = await reader.read(100)
        if not data:
            break

        response = data.decode()
        print(f"recived: {response}")

async def send(writer):
    while True:
        message = await asyncio.to_thread(input, "enter message: ")
        writer.write(message.encode())
        await writer.drain()

async def main():
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)

    receiver = asyncio.create_task(receive(reader))
    sender = asyncio.create_task(send(writer))

    await asyncio.gather(receiver, sender)

    writer.close()
    await writer.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())

