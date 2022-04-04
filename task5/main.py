import socket
import asyncio
import aioping
import graphviz

list_ips = {}


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


async def scan_ip(ip):
    try:
        delay = await aioping.ping(ip, timeout=2)
        list_ips[ip] = round(delay * 1000, 3)
    except TimeoutError:
        return


async def main():
    my_ip = get_ip()
    prefix = '.'.join(my_ip.split('.')[:-1])
    await asyncio.gather(*[scan_ip(prefix + '.' + str(i)) for i in range(1, 256) if i != int(my_ip.split('.')[-1])])
    dot = graphviz.Digraph('Network', format='pdf')

    dot.node(my_ip)
    for ip in list_ips:
        dot.node(ip)
        dot.edge(tail_name=my_ip, head_name=ip, label=str(list_ips[ip]))
    dot.render('my-network')

if __name__ == "__main__":
    asyncio.run(main())
