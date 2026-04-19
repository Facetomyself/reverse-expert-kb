#!/usr/bin/env python3
import asyncio

LISTEN_HOST = '0.0.0.0'
LISTEN_PORT = 18783
TARGET_HOST = '127.0.0.1'
TARGET_PORT = 18781

async def pipe(reader, writer):
    try:
        while True:
            data = await reader.read(65536)
            if not data:
                break
            writer.write(data)
            await writer.drain()
    finally:
        try:
            writer.close()
        except Exception:
            pass

async def handle(client_reader, client_writer):
    try:
        server_reader, server_writer = await asyncio.open_connection(TARGET_HOST, TARGET_PORT)
    except Exception:
        client_writer.close()
        return
    await asyncio.gather(
        pipe(client_reader, server_writer),
        pipe(server_reader, client_writer),
    )

loop = asyncio.get_event_loop()
server_coro = asyncio.start_server(handle, LISTEN_HOST, LISTEN_PORT, loop=loop)
server = loop.run_until_complete(server_coro)
try:
    loop.run_forever()
finally:
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
