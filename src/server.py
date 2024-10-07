import socket
import threading
import sys

# Function to handle each client connection
def handle_client(connection, address):
    try:
        print(f"Connection from {address} has been established")
        
        # Set a timeout for receiving data (e.g., 5 seconds)
        connection.settimeout(5.0)

        # Receive the file data from the client
        file_data = connection.recv(4096)

        if file_data == b'':  # Check if no data is received (client closed connection)
            response = "No data received or file is empty."
        else:
            # Count alphabetic characters (A-Z, a-z)
            alphabetic_count = sum(c.isalpha() for c in file_data.decode('utf-8', errors='ignore'))
            response = f"Number of alphabetic characters: {alphabetic_count}"

        # Send the response back to the client
        connection.sendall(response.encode('utf-8'))

    except socket.timeout:
        # Handle the case where no data was received before timeout
        print(f"Timeout from {address}: No data received.")
        response = "No data received before timeout."
        connection.sendall(response.encode('utf-8'))
    except Exception as e:
        print(f"Error handling client {address}: {e}")
    finally:
        connection.close()

def start_server(port):
    # Create a TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('', int(port)))
        server_socket.listen(5)
        print(f"Server listening on port {port}")

        while True:
            # Accept incoming client connections
            client_socket, client_address = server_socket.accept()

            # Handle the client in a new thread
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)

    port = sys.argv[1]
    start_server(port)
