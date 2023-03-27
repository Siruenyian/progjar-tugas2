import socket
import ssl
import re

from bs4 import BeautifulSoup

HOST = 'www.its.ac.id'
HOST2 = 'classroom.its.ac.id'
PORT = 443

def connect(HOST):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, 443)
    client_socket.connect(server_address)
    # We have to warp this since it's a https(?)
    client_socket = ssl.wrap_socket(
        client_socket, ssl_version=ssl.PROTOCOL_SSLv23)
    request_header = 'GET / HTTP/1.1\r\nHost:{0}\r\n\r\n'.format(
        HOST)
    client_socket.send(request_header.encode())
    response = ''
    while True:
        received = client_socket.recv(1028)
        if not received:
            break
        response += received.decode('utf-8')
    client_socket.close()

    document = response.split('\r\n\r\n')
    headers = document[0]
    # in bytes
    htmldoc = document[1].encode()

    output = {}
    # Regex to sokit key value of headers
    result = re.findall(r"([\w-]+): (.*)\r", headers[1:])
    output = dict(result)
    if output["Content-Type"]:
        output["Content-Type"] = output["Content-Type"].split(' ')
    output["status"] = headers.split('\r\n')[0].split(" ", 1)
    return output, htmldoc


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
        HOST, PORT,
        'GET / HTTP/1.1\r\nHost: {}\r\nAccept-Encoding: utf-8\r\n\r\n'.format(HOST).encode(),
        True
    )

    response_list = response.split('\r\n\r\n')
    response_header = response_list[0].split('\r\n')

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
        HOST2, PORT,
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

    # Nomor 5 : Parsing HTML
    response = get_response(
        HOST2, PORT,
        'GET / HTTP/1.1\r\nHost: {}\r\nAccept-Encoding: utf-8\r\n\r\n'.format(HOST2).encode()
    )

    response_list = response.split('\r\n\r\n', 1)
    response_header = response_list[0].split('\r\n')
    response_content = response_list[1]

    # headers, body = connect('classroom.its.ac.id')
    soup = BeautifulSoup(response_content, 'html.parser')
    # print(soup.prettify())

    menus = soup.findAll('a', attrs={'class': 'dropdown-toggle nav-link'})

    for menu in menus:
        print(menu.getText().strip())

        dropdown_menu = menu.findNextSibling('div')
        sub_menus = dropdown_menu.findAll('a')
        for sub_menu in sub_menus:
            print('\t{}'.format(sub_menu.getText().strip()))

        # print(a.get_text(separator='-'))

    # print([a for a in x])


    # ssl_socket.close()
