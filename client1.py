import ssl
import socket
import logging

def sort_data_and_send_to_server():
    try:
        server_address = ('192.168.1.11', 12345)
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        with socket.create_connection(server_address) as client_socket:
            with context.wrap_socket(client_socket, server_hostname=server_address[0]) as secure_client_socket:
                secure_client_socket.send('sort'.encode())
                data_to_sort = eval(secure_client_socket.recv(1024).decode())
                sorted_data = sorted(data_to_sort)
                logging.info("Sorted data: %s ", sorted_data)
                secure_client_socket.send(str(sorted_data).encode())

                sum_result = sum(data_to_sort)
                logging.info("Sum of array elements: %d", sum_result)
                secure_client_socket.send(str(sum_result).encode())

    except Exception as e:
        logging.error("Error sorting data and sending to server: %s", e)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sort_data_and_send_to_server()