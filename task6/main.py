import socket
import threading

host = "localhost"
list_addresses = []


def port_scan(port):
    try:
        s = socket.socket()
        s.connect((host, port))
        list_addresses.append((host, port))
    except OSError:
        s.close()
        return
    finally:
        s.close()


if __name__ == "__main__":
    for i in range(1, 65536):
        thread = threading.Thread(target=port_scan, args=[i])
        thread.start()
    print(list_addresses)
