import socket

HOST, PORT = 'localhost', 8090


def get_response(host, port, request, only_header=False):
    csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    csock.connect(server_address)

    csock.send(request)

    response = ''
    while True:
        received = csock.recv(1024)
        decoded = received.decode('utf-8')

        if decoded.endswith('\0'):
            response += decoded[:-1]
            break
        else:
            response += decoded

        if only_header and received.decode('utf-8').find('\r\n\r\n') != -1:
            break

    csock.close()

    return response


def main():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        print('Welcome to our server, input path to access\n')
        path = input('>> ')
        response = get_response(
            HOST, PORT,
            'GET {} HTTP/1.1\r\nHost: {}\r\n\r\n'.format(path, HOST).encode('utf-8')
        )
        response_list = response.split('\r\n\r\n', 1)
        response_headers = response_list[0].split('\r\n')
        response_content = response_list[1]

        version_status = response_headers[0].split(' ', 1)
        status = version_status[1]

        print('Status :', status)
        print(response_content)

        client_socket.close()
    except Exception as msg:
        print(msg)


if __name__ == "__main__":
    main()
