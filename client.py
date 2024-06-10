
import socket

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 9999))

    while True:
        response = client.recv(1024)
        print(response.decode(), end='')

        if 'Final balance' in response.decode():
            break

        data = input()
        client.send(data.encode())

    client.close()

if __name__ == "__main__":
    start_client()
