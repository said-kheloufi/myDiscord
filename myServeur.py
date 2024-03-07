import socket
import threading

# Define the server address and port
HOST = '127.0.0.1'
PORT = 5555
# List to keep track of connected clients (active sessions)
active_clients = [] 

# Function to listen for messages from a specific client
def listen_for_messages(client, username):
    while True:
        # Receive a message from the client
        message = client.recv(2048).decode('utf-8')
        if message != '':
            # If the message is not empty, prepend the username and send it to all clients
            final_msg = username + '~' + message
            send_messages_to_all(final_msg)
        else:
            print(f"The message send from client {username} is empty")

# Function to send a message to a specific client
def send_message_to_client(client, message):
    client.sendall(message.encode())

# Function to send a message to all connected clients
def send_messages_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1], message)

# Function to handle a new client connection
def client_handler(client):
    while True:
        # Receive the username from the client
        username = client.recv(2048).decode('utf-8')
        if username != '':
            # If the username is not empty, add the client to the list of active clients
            active_clients.append((username, client))
            prompt_message = "SERVER~" + f"{username} added to the chat"
            send_messages_to_all(prompt_message)
            break
        else:
            print("Client username is empty")

    # Start a new thread to listen for messages from this client
    threading.Thread(target=listen_for_messages, args=(client, username, )).start()

# Main function to start the server
def main():
    # Create a new socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Try to bind the socket to the host and port
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")

    # Start listening for connections
    server.listen()

    while True:
        # Accept a new client connection
        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")

        # Start a new thread to handle the client
        threading.Thread(target=client_handler, args=(client, )).start()

# If the script is run directly (not imported as a module), call the main function
if __name__ == '__main__':
    main()
