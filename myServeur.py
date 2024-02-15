# Import necessary modules
import socket
import threading

# Define constants
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 1234  # The port used by the server
active_clients = []  # List to keep track of active clients

# Function to listen for messages from a client
def listen_for_messages(client, username):
    while True:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            final_msg = username + '~' + message
            send_messages_to_all(final_msg)
        else:
            print(f"The message send from client {username} is empty")

# Function to send a message to a client
def send_message_to_client(client, message):
    client.sendall(message.encode())

# Function to send a message to all clients
def send_messages_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1], message)

# Function to handle a new client connection
def client_handler(client):
    while True:
        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            prompt_message = "SERVER~" + f"{username} added to the chat"
            send_messages_to_all(prompt_message)
            break
        else:
            print("Client username is empty")

    threading.Thread(target=listen_for_messages, args=(client, username, )).start()

# Main function
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")

    server.listen()

    while True:
        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")
        threading.Thread(target=client_handler, args=(client, )).start()

if __name__ == '__main__':
    main()
