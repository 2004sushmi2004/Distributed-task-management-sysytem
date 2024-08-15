import ssl
import socket
import logging

def receive_file_and_process():
    try:
        server_address = ('192.168.1.11', 12345)
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        with socket.create_connection(server_address) as client_socket:
            with context.wrap_socket(client_socket, server_hostname=server_address[0]) as secure_client_socket:
                secure_client_socket.send('file'.encode())
                received_data = secure_client_socket.recv(1024).decode()

                with open('received_file.txt', 'w') as file:
                    file.write(received_data)

                logging.info("Contents of received file (before capitalization): %s", received_data)

                # Capitalize the received file content
                capitalized_contents = received_data.upper()

                logging.info("Contents of received file (after capitalization): %s", capitalized_contents)

                # Count words in the capitalized content
                word_count = len(capitalized_contents.split())

                # Send capitalized content and word count back to server
                secure_client_socket.send(capitalized_contents.encode())
                secure_client_socket.send(str(word_count).encode())
    except Exception as e:
        logging.error("Error receiving file and processing: %s", e) 

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    receive_file_and_process()