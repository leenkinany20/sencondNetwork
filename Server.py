import socket
import threading

# Pre-defined bank accounts
accounts = {
    '123456': {'pin': '1234', 'balance': 1000.0},
    '654321': {'pin': '4321', 'balance': 500.0}
}

# Function to handle client connections
def handle_client(client_socket):
    try:
        client_socket.send(b"Enter your account number: ")
        account_number = client_socket.recv(1024).decode().strip()

        client_socket.send(b"Enter your PIN: ")
        pin = client_socket.recv(1024).decode().strip()

        if account_number in accounts and accounts[account_number]['pin'] == pin:
            client_socket.send(b"Authenticated")
            while True:
                client_socket.send(b"Enter command (balance/deposit/withdraw/exit): ")
                command = client_socket.recv(1024).decode().strip()

                if command == 'balance':
                    balance = accounts[account_number]['balance']
                    client_socket.send(f"Your balance is {balance}\n".encode())

                elif command == 'deposit':
                    client_socket.send(b"Enter amount to deposit: ")
                    amount = float(client_socket.recv(1024).decode().strip())
                    accounts[account_number]['balance'] += amount
                    client_socket.send(b"Deposit successful\n")

                elif command == 'withdraw':
                    client_socket.send(b"Enter amount to withdraw: ")
                    amount = float(client_socket.recv(1024).decode().strip())
                    if amount <= accounts[account_number]['balance']:
                        accounts[account_number]['balance'] -= amount
                        client_socket.send(b"Withdrawal successful\n")
                    else:
                        client_socket.send(b"Insufficient funds\n")

                elif command == 'exit':
                    balance = accounts[account_number]['balance']
                    client_socket.send(f"Final balance: {balance}\n".encode())
                    break
                else:
                    client_socket.send(b"Invalid command\n")
        else:
            client_socket.send(b"Authentication failed\n")
    finally:
        client_socket.close()

# Main server function
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print("Server listening on port 9999")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
