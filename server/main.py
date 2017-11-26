import os
import sys
import argparse
import json
import logging
import select
import time
from socket import *
# Костыль, который нужно убрать не понимаю почему когда из консоли стартую
# main.py -w получаю ImportError client Not found
sys.path.append('/home/leming/Documents/PycharmProject/Messenger')
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
            # Словарь для хранения связи имя клиента - сокет
            self.named_socket = {}
            # Словарь для клиентов, которые подключаются к серверу
            self._clients = []
        except OSError as start_server_error:
            print("Ошибка при запуске сервера: {}".format(start_server_error))
            sys.exit(1)

    @log
    def start(self):
        while True:
            try:
                conn, addr = self.sock.accept()
                data = conn.recv(1024)
                self.client_registrator(conn, data)
            except OSError as e:
                pass
            else:
                self._clients.append(conn)
            finally:
                r = []
                w = []
                try:
                    r, w, e = select.select(self._clients, self._clients, [], 0)
                except:
                    pass
                request_msg = self.read_requests(r, self._clients)
                self.write_responses(request_msg, w, self._clients)
    @log
    def read_requests(self, r_clients, all_clients):
        """Чтение запросов из списка клиентов"""
        messages = []
        for sock in r_clients:
            try:
                data = sock.recv(MAX_DATA_RECEIVE)
                # Добавляем в список сообщение и кто прислал
                messages.append((data, sock))
            except:
                # Почему то раняет сервер если клиент через ctrl + c отключился
                # IndexError: tuple index out of range
                print('Клиент {} {} отключился'.format(sock.fileno()), sock.getpeername())
                all_clients.remove(sock)
        return messages

    @log
    def write_responses(self, messages, w_clients, all_clients):
        """Эхо-ответ сервера клиентам, от которых были запросы"""

        for message in messages:
            # Парсим входящее сообщение
            self.parse_data_from_clietn(message[1], message[0])

    @log
    def stop(self):
        self.sock.close()

    def client_registrator(self, client, data):
        unserialized_data = json.loads(data.decode("utf-8"))

        # presence msg and add new client
        if unserialized_data.get('action').startswith('presence'):
            account_name = unserialized_data.get('user').get('account_name')
            # Нужно добавить клиента в именнованный словарь сокетов
            self.named_socket[account_name] = client
            # Добавляем клиента в базу
            self.storage.add_client(account_name, client.getpeername()[0])
            self.storage.commit()
            # Послылаем ему ответ что все хорошо и он успешно подключился
            client.send(self.protocol.good_resp())

    def parse_data_from_clietn(self, client, data):
        """Processing Custom Messages"""
        try:
            unserialized_data = json.loads(data.decode("utf-8"))
            # add contact
            if unserialized_data.get('action').startswith('add_contact'):
                user_name = unserialized_data.get('user_name')
                contact_name = unserialized_data.get('contact_name')
                self.storage.add_contact(user_name, contact_name)
                # Как лучше обработать исключение если такой клиент существует в БД?
                self.storage.commit()
                client.send(self.protocol.good_resp())
            # get contact from server storage
            elif unserialized_data.get('action').startswith('get_contact'):
                account_name = unserialized_data.get('user')
                contact_list = self.storage.get_contact_list(account_name)
                # send response to client
                client.send(self.protocol.count_contacts_resp(len(contact_list), contact_list))
            # msg from client to another client
            elif unserialized_data.get('action').startswith('msg'):
                to = unserialized_data.get('to')
                to = self.named_socket.get(to)
                to.send(json.dumps(unserialized_data).encode("utf-8"))

            # don't work
            # disconnect client
            elif unserialized_data.get('action').startwith('quit'):
                print("Клиент хочет отключиться!")
                client.close()
            else:
                raise BadRequestFromClientError("TestUsr")
        except BadRequestFromClientError:
            client.send(self.protocol.bad_resp(400))
        except AttributeError:
            client.send(self.protocol.bad_resp(400))


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
