import asyncio
class TcpConnector(asyncio.Transport):
    def connection_made(self, transport):
        transport.close()
    def connection_lost(self, exc):
        pass

async def try_connect(ip, port):
    loop = asyncio.get_running_loop()
    await asyncio.wait_for(loop.create_connection(TcpConnector, ip, port), 0.5)
    return port
async def main():
    ip = '127.0.0.1'
    portrange = (1, 9000)
    loop = asyncio.get_running_loop()
    #ports_open = []
    coroutines = []
    def callback(coroutine):
        coroutines.remove(coroutine)
        #if not coroutine.exception():
        try:
            print(coroutine.result())
        except TimeoutError:
            pass
    for port in range(*portrange):
        #print(f'{port}')
        #try:
            #await try_connect(ip, port)
            coroutines.append(loop.create_task(try_connect(ip, port)))
            coroutines[-1].add_done_callback(callback)
            loop.create_task(try_connect(ip, port))

        #except ConnectionRefusedError:
            #pass
        #else:
            #ports_open.append(port)
        #asyncio.gather(*coroutines)
    while len(coroutines)  > 0:
        await asyncio.sleep(1)
    #print(ports_open)
asyncio.run(main())