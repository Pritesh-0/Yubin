import asyncio
import sys


async def read(reader):
    while True:
        #try:
            #async with asyncio.timeout(5):
                #print('r')
                data = await reader.read(100)
                if not data:
                    break

                message = data.decode()
                print(f"Received: {message}")
                sys.stdout.flush()
        #except TimeoutError:
            #print('timeout in read')

async def write(writer):
    while True:
        #try:
            #async with asyncio.timeout(5):
                #print('w')
                message = await asyncio.to_thread(input,"enter message: ")


                writer.write(message.encode())
                await writer.drain()
                sys.stdout.flush()
        #except TimeoutError:
            #print('timeout in write')
        
        #await asyncio.sleep(1)

async def main():
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)

    try:
        task_read = asyncio.create_task(read(reader))
        task_write = asyncio.create_task(write(writer))

        await asyncio.gather(task_read, task_write)
    finally:
        writer.close()
        await writer.wait_closed()

if __name__ == '__main__':
    asyncio.run(main())

