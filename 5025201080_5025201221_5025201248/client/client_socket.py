import socket
import ssl

HOST = 'www.its.ac.id'
PORT = 443

if __name__ == "__main__":

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context()
    ssl_socket = context.wrap_socket(client_socket, server_hostname=HOST)
    server_address = (HOST, PORT)
    ssl_socket.connect(server_address)

    request_header = 'GET / HTTP/1.1\r\nHost: {}\r\nAccept-Encoding: utf-8\r\n\r\n'.format(HOST).encode()
    ssl_socket.send(request_header)

    response = ''
    while True:
        received = ssl_socket.recv(1024)
        if not received:
            break
        response += received.decode('utf-8')

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

    # Nomor 4 : Charset
    charset_index = content_type.find('charset')
    charset = content_type[charset_index+8:]
    print('Charset :', charset)

    ssl_socket.close()
