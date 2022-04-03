import socket
import asyncio
import aioping


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


async def scan_ip(ip):
    try:
        delay = await aioping.ping(ip, timeout=2)
        print(f'address: {ip}; ping: {delay * 1000}')
    except TimeoutError:
        print(f'address: {ip}; timeout')


async def main():
    my_ip = get_ip()
    prefix = '.'.join(my_ip.split('.')[:-1])
    await asyncio.gather(*[scan_ip(prefix + '.' + str(i)) for i in range(1, 256) if i != my_ip.split('.')[-1]])

if __name__ == "__main__":
    asyncio.run(main())
