import asyncio

def readm(reader):
    data = await reader.read(100)
    
def writem(writer,msg):
    writer.write(msg.encode())
    await writer.drain()

async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8888)

    #print(f'Send: {message!r}')
    #writer.write(message.encode())
    #await writer.drain()
    readm(reader)
    #data = await reader.read(100)
    #print(f'Received: {data.decode()!r}')
    writem(writer,message)
    #print('Close the connection')
    writer.close()
    await writer.wait_closed()

asyncio.run(tcp_echo_client('Hello World!'))

