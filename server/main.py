import os
import sys
import argparse
import json
import logging
import select
import time
from socket import *

from config.constants import LOG_DIR
from server.errors import BadRequestFromClientError
from log.decorators import Log
from log.log_config import setup_logger
from server.repository.storage import ServerStorage
from protocols.jim.jimprotocol import JIMProtocolServer

MAX_DATA_RECEIVE = 1024
MAX_CLIENT_CONNECTION = 20

# Log сервера
setup_logger('server', os.path.join(LOG_DIR, 'server.log'))
server_log = logging.getLogger('server')
# Создание класса декоратора для логирования функций
log = Log(server_log)


class Server:

    def __init__(self, addr, port):
        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.bind((addr, port))
            self.sock.listen(MAX_CLIENT_CONNECTION)
            self.sock.settimeout(0.2)
            # Storage for server
            self.storage = ServerStorage('ServerStorage')
            # Using protocol
            self.protocol = JIMProtocolServer()
        except OSError as start_server_error:
            print("Ошибка при запуске сервера: {}".format(start_server_error))
            sys.exit(1)

    @log
    def start(self):
        clients = []
        while True:
            try:
                conn, addr = self.sock.accept()
                data = conn.recv(1024)
                print(data)
                self.parse_data_from_clietn(conn, addr, data)
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
    @log
    def read_requests(self, r_clients, all_clients):
        """Чтение запросов из списка клиентов"""
        messages = []
        for sock in r_clients:
            try:
                data = sock.recv(1024).decode('utf-8')
                messages.append(data)
            except:
                # Почему то раняет сервер если клиент через ctrl + c отключился
                # IndexError: tuple index out of range
                print('Клиент {} {} отключился'.format(sock.fileno()), sock.getpeername())
                all_clients.remove(sock)
        return messages

    @log
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
    @log
    def stop(self):
        self.sock.close()

    @log
    def parse_data_from_clietn(self, client, addr, data):
        """Processing Custom Messages"""
        try:
            unserialized_data = json.loads(data.decode("utf-8"))
            account_name = unserialized_data.get('user').get('account_name')
            # presence msg and add new client
            if unserialized_data.get('action').startswith('presence'):
                self.storage.add_client(account_name)
                self.storage.commit()
                client.send(self.protocol.good_resp())
            # add contact
            elif unserialized_data.get('action').startswith('add_contact'):
                user_name = unserialized_data.get('user_name')
                contact_name = unserialized_data.get('contact_name')
                self.storage.add_contact(user_name, contact_name)
                # Как лучше обработать исключение если такой клиент существует в БД?
                self.storage.commit()
                client.send(self.protocol.good_resp())
            # get contact from server storage
            elif unserialized_data.get('action').startswith('get_contact'):
                contact_list = self.storage.get_contact_list(account_name)
                # send response to client
                client.send(self.protocol.count_contacts_resp(len(contact_list)))
                client.send(self.protocol.contact_resp(contact_list))
            # print msg from client
            elif unserialized_data.get('action').startswith('msg'):
                print(unserialized_data)
            # don't work
            # disconnect client
            elif unserialized_data.get('action').startwith('quit'):
                client.close()
            else:
                raise BadRequestFromClientError(account_name)
        except BadRequestFromClientError:
            client.send(self.protocol.bad_resp(400, account_name))


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
