import json
import sys
import time
import argparse
import select
from multiprocessing import Queue
import queue
from errors import BadRequestFromClientError
from socket import *

MAX_DATA_RECEIVE = 1024
MAX_CLIENT_CONNECTION = 20


class Server:

    def __init__(self, addr, port):
        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.bind((addr, port))
            self.sock.listen(MAX_CLIENT_CONNECTION)
            self.sock.settimeout(0.2)
        except OSError as start_server_error:
            print("Ошибка при запуске сервера: {}".format(start_server_error))
            sys.exit(1)

    def start(self):
        clients = []
        while True:
            try:
                conn, addr = self.sock.accept()
            except OSError as e:
                pass
            else:
                clients.append(conn)
            finally:
                r = []
                w = []
                try:
                    r, w, e = select.select(clients, clients, [], 0)
                except:
                    pass
                request_msg = self.read_requests(r, clients)
                self.write_responses(request_msg, w, clients)

    def read_requests(self, r_clients, all_clients):
        """Чтение запросов из списка клиентов"""
        messages = []
        for sock in r_clients:
            try:
                data = sock.recv(1024).decode('utf-8')
                messages.append(data)
            except:
                print('Клиент {} {} отключился'.format(sock.fileno()), sock.getpeername())
                all_clients.remove(sock)
        return messages

    def write_responses(self, messages, w_clients, all_clients):
        """Эхо-ответ сервера клиентам, от которых были запросы"""

        for sock in w_clients:
            for message in messages:
                try:
                    sock.send(str(message).encode("utf-8"))
                except:
                    print('Клиент {} {} отключился'.format(sock.fileno()), sock.getpeername())
                    sock.close()
                    all_clients.remove(sock)

    def stop(self):
        self.sock.close()

    def parse_data_from_clietn(self, client, addr, data):
        try:
            unserialized_data = json.loads(data.decode("utf-8"))
            account_name = unserialized_data.get('user').get('account_name')
            if unserialized_data.get('action').startswith('presence'):

                print("Клиент {} подключился к серверу с IP: {} <{}>".format(
                    account_name, addr[0], unserialized_data.get('time'))
                )
                Server.send_good_response_to_client(client, 200, account_name)
            elif unserialized_data.get('action').startswith('msg'):
                print(unserialized_data)
            else:
                raise BadRequestFromClientError(account_name)
        except BadRequestFromClientError:
            self.send_bad_response_to_client(client, 400, account_name)

    def send_good_response_to_client(self, client, code, account_name):
        response_msg = {
            "response": code,
            "time": int(time.time()),
            "alert": "OK"
        }
        serialized_response = json.dumps(response_msg).encode("utf-8")
        try:
            client.send(serialized_response)
        except OSError as err:
            print("Ошибка отправки сообщения клиенту {}: {}".format(account_name, err))

    def send_bad_response_to_client(self, client, code, account_name):
        response_msg = {
            "response": code,
            "time": int(time.time()),
            "error": "Bad request"
        }
        serialized_response = json.dumps(response_msg).encode("utf-8")
        try:
            client.send(serialized_response)
        except OSError as err:
            print("Ошибка при отправки сообщения клиенту {}: {}".format(account_name, err))


def create_parser():
    parser = argparse.ArgumentParser(
        prog='server',
        description=
        """
        Серверная часть мессенджера.
        """,
        epilog=
        """
        (c) September 2017.
        """
    )
    parser.add_argument(
        '-p', '--port', type=int, default=7777, help="""
        Порт на котором будет работать сервер и ожидать подключения от клиентов"""
    )
    parser.add_argument(
        '-a', '--addr', default='127.0.0.1', help="""
        IP-адрес на котором будет работать сервер.
        """
    )
    return parser


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    addr = namespace.addr
    port = namespace.port
    server = Server(addr, port)
    server.start()
