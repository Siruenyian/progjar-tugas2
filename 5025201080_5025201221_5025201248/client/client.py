import sys
import socket

HOST, PORT = 'localhost', 9999


def main(e):
    try:

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        client_socket.connect(HOST, PORT)
        print('Input command\n')
        message = input('>> ')
        client_socket.send(bytes(message, encoding='utf-8'))
        response = ''
        while True:
            received = client_socket.recv(1024)
            if not received:
                break
            response += received.decode('utf-8')
        print(response)
        client_socket.shutdown(socket.SHUT_RDWR)
        client_socket.close()
    except Exception as msg:
        print(msg)


if __name__ == "__main__":
    main("testing123")
