import ssl
import socket
import logging
from queue import Queue
from threading import Thread

def send_file_to_client(client_socket):
    try:
        with open('data.txt', 'rb') as file:
            data = file.read(1024)
            while data:
                client_socket.send(data)
                data = file.read(1024)
    except FileNotFoundError:
        logging.error("File 'data.txt' not found.")

def receive_sorted_data(client_socket):
    try:
        # Prompt the user to enter a list of elements separated by commas
        input_str = input("Enter a list of elements separated by commas: ")

        # Convert the input string to a list of integers
        data_to_sort = [int(x.strip()) for x in input_str.split(",")]

        # Send the list to the client for sorting
        client_socket.send(str(data_to_sort).encode())

        # Receive the sorted data from the client
        sorted_data = client_socket.recv(1024).decode()
        logging.info("Sorted data received from client: %s", sorted_data)

        # Receive the sum of array elements from the client
        sum_result = client_socket.recv(1024).decode()
        logging.info("Sum of array elements received from client: %s", sum_result)

    except Exception as e:
        logging.error("Error receiving and processing data: %s", e)


def receive_and_process_file(client_socket):
    try:
        received_data = client_socket.recv(1024).decode()
        logging.info("Contents of file received from client: %s", received_data)

        # Wait for the word count from the client
        word_count = client_socket.recv(1024).decode()
        logging.info("Word count received from client: %s", word_count)
    except Exception as e:
        logging.error("Error receiving and processing file: %s", e)

def handle_client(client_socket, task_queue):
    try:
        task_type = client_socket.recv(1024).decode()

        if task_type == 'file':
            task_queue.put((client_socket, 'file'))
        elif task_type == 'sort':
            task_queue.put((client_socket, 'sort'))
        else:
            logging.error("Unknown task type received.")
    except Exception as e:
        logging.error("Error handling client: %s", e)

def task_dispatcher(task_queue):
    while True:
        if not task_queue.empty():
            client_socket, task_type = task_queue.get()
            if task_type == 'file':
                send_file_to_client(client_socket)
                logging.info("File sent to client.")
                receive_and_process_file(client_socket)
            elif task_type == 'sort':
                receive_sorted_data(client_socket)
            client_socket.close()

def main():
    logging.basicConfig(level=logging.INFO)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('192.168.43.119', 12345))
    server_socket.listen(5)  # Listen for multiple clients
    logging.info("Server listening...")

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    secure_server_socket = context.wrap_socket(server_socket, server_side=True)

    task_queue = Queue()
    dispatcher_thread = Thread(target=task_dispatcher, args=(task_queue,))
    dispatcher_thread.start()

    while True:
        client_socket, _ = secure_server_socket.accept()
        client_thread = Thread(target=handle_client, args=(client_socket, task_queue))
        client_thread.start()

    secure_server_socket.close()

if __name__== "__main__":
    main()