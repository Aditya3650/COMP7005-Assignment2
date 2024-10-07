import socket
import sys

def send_file_to_server(server_ip, server_port, file_path):
    try:
        # Open the file and read its contents
        with open(file_path, 'rb') as file:
            file_data = file.read()

        # Create a TCP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Connect to the server
            s.connect((server_ip, int(server_port)))
            print(f"Connected to {server_ip}:{server_port}")

            # Send the file data
            s.sendall(file_data)
            print(f"File '{file_path}' sent to the server")

            # Receive the response from the server (count of alphabetic characters)
            response = s.recv(1024).decode('utf-8')
            print(f"Response from server: {response}")

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python client.py <server_ip> <server_port> <file_path>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = sys.argv[2]
    file_path = sys.argv[3]

    send_file_to_server(server_ip, server_port, file_path)
