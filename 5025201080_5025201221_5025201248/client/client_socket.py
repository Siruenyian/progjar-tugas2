import socket
import ssl

HOST = 'www.its.ac.id'
HOST2 = 'classroom.its.ac.id'
PORT = 443


def get_response(host, port, request, only_header=False):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context()
    ssl_socket = context.wrap_socket(client_socket, server_hostname=host)
    server_address = (host, port)
    ssl_socket.connect(server_address)

    ssl_socket.send(request)

    response = ''
    while True:
        received = ssl_socket.recv(1024)
        if not received:
            break

        response += received.decode('utf-8')

        if only_header and received.decode('utf-8').find('\r\n\r\n') != -1:
            break

    ssl_socket.close()

    return response

if __name__ == "__main__":

    # Request to its.ac.id for number 1 - 3
    response = get_response(
        HOST, 443,
        'GET / HTTP/1.1\r\nHost: {}\r\nAccept-Encoding: utf-8\r\n\r\n'.format(HOST).encode()
    )

    response_list = response.split('\r\n\r\n')
    response_header = response_list[0].split('\r\n')
    response_content = ''.join(response_list[1:])

    print("Request to ", HOST)

    version_status = response_header[0].split(' ', 1)
    # Nomor 1 : status code
    print('Status :', version_status[1])

    # Nomor 2 : Content type
    content_type = response_header[3]
    print('Content Type :', content_type)

    # Nomor 3 : HTTP Version
    print('HTTP Version :', version_status[0])

    # Request to classroom.its.ac.id for number 4
    response = get_response(
        HOST2, 443,
        'GET / HTTP/1.1\r\nHost: {}\r\nAccept-Encoding: utf-8\r\n\r\n'.format(HOST2).encode(),
        True
    )

    print("\nRequest to", HOST2)


    # Nomor 4 : Charset
    response_list = response.split('\r\n\r\n')
    response_header = response_list[0].split('\r\n')
    content_type = response_header[3]
    charset_index = content_type.find('charset')
    charset = content_type[charset_index+8:]
    print('Charset :', charset)

    # ssl_socket.close()
