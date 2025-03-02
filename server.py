import socket
import threading

# Server configuration
HOST = '10.0.2.15'  # Your IPv4 address
PORT = 55555

# Create a socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# Lists for clients and their nicknames
clients = []
nicknames = []

# Broadcast message to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handle individual client connections
def handle(client):
    while True:
        try:
            # Broadcast messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # Remove and close client
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break

# Main function to receive clients
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # Request and store nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print and broadcast nickname
        print(f'Nickname of the client is {nickname}!')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))

        # Start handling thread for client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

# The entry point of the program
if __name__ == "__main__":
    print("Server is listening...")
    receive()

