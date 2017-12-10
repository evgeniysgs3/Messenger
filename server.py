import os
import sys
import argparse
import json
import logging
import select
from socket import *

from src.server.errors import BadRequestFromClientError, ClientDisconected
from src.log.log_config import setup_logger
from src.protocols.jim.jimprotocol import JIMProtocolServer
from src.server.repository.storage import ServerStorage
from src.config.constants import LOG_DIR

from src.log.decorators import Log

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
            self.addr = addr
            self.port = port
            # Запускаем сервер
            self.sock = self._start()

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

    def _start(self):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind((self.addr, self.port))
        sock.listen(MAX_CLIENT_CONNECTION)
        sock.settimeout(0.2)
        return sock

    def _get_connection(self):
        try:
            conn, addr = self.sock.accept()
            data = conn.recv(MAX_DATA_RECEIVE)
            if data:
                account_name = self.client_registrator(conn, data)
        except OSError as e:
            pass
        else:
            self._clients.append(conn)
            # Нужно добавить клиента в именнованный словарь сокетов
            self.named_socket[account_name] = conn
        finally:
            wait = 0
            r = []
            w = []
            try:
                r, w, e = select.select(self._clients, self._clients, [], wait)
            except:
                pass # Ничего не делать, если какой-то клиент отключился

            request_msg = self.read_requests(r)
            self.write_responses(request_msg)

    def main_loop(self):
        while True:
            self._get_connection()

    def read_requests(self, r_clients):
        """Чтение запросов из списка клиентов"""
        messages = []
        for sock in r_clients:
            try:
                # Получаем входящие сообщения
                data = sock.recv(MAX_DATA_RECEIVE)
                # Добавляем в список сообщение и кто прислал
                messages.append((data, sock))
            except:
                # Почему то раняет сервер если клиент через ctrl + c отключился
                # IndexError: tuple index out of range
                print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()[0]))
                self._clients.remove(sock)
        # Возвращаем словарь
        return messages

    def write_responses(self, messages):
        """Эхо-ответ сервера клиентам, от которых были запросы"""

        for message, sender in messages:
            # Парсим входящее сообщение
            self.parse_data_from_clietn(message, sender)

    def client_registrator(self, client, data):
        try:
            if data:
                unserialized_data = json.loads(data.decode("utf-8"))
                print(unserialized_data)
                # presence msg and add new client
                if unserialized_data.get('action').startswith('presence'):
                    account_name = unserialized_data.get('user').get('account_name')
                    ip_addr_client = client.getpeername()[0]
                    print("Пользователь: {} IP: {} подключен.".format(account_name, ip_addr_client))
                    # Добавляем клиента в базу
                    self.storage.add_client(account_name, ip_addr_client)
                    self.storage.commit()
                    # Послылаем ему ответ что все хорошо и он успешно подключился
                    client.send(self.protocol.good_resp())
                    return account_name
                # Плохой запрос
                else:
                    client.send(self.protocol.bad_resp(400))
            else:
                # Клиент отключился при закрытии приложения посылается 0 bytes
                raise ClientDisconected(client.getpeername()[0])
        except ClientDisconected:
            print("Catch my_exception from client_registration")
            self._clients.remove(client)

    def parse_data_from_clietn(self, data, sender):
        """Processing Custom Messages"""
        try:
            if data:
                unserialized_data = json.loads(data.decode("utf-8"))
                print(unserialized_data)
                # add contact
                if unserialized_data.get('action').startswith('add_contact'):
                    user_name = unserialized_data.get('user_name')
                    contact_name = unserialized_data.get('contact_name')
                    self.storage.add_contact(user_name, contact_name)
                    # Как лучше обработать исключение если такой клиент существует в БД?
                    self.storage.commit()
                    sender.send(self.protocol.good_resp())

                # get contact from server storage
                elif unserialized_data.get('action').startswith('get_contact'):
                    account_name = unserialized_data.get('user')
                    contact_list = self.storage.get_contact_list(account_name)
                    # send response to client
                    sender.send(self.protocol.count_contacts_resp(len(contact_list), contact_list))

                # msg from client to another client
                elif unserialized_data.get('action').startswith('msg'):
                    to = unserialized_data.get('to')
                    to = self.named_socket.get(to)
                    to.send(json.dumps(unserialized_data).encode("utf-8"))

                # disconnect client
                elif unserialized_data.get('action').startwith('quit'):
                    print("Клиент хочет отключиться!")
                    self._clients.remove(sender)
                    sender.close()
                else:
                    raise BadRequestFromClientError(sender.getpeername()[0])
            else:
                raise ClientDisconected(sender.getpeername()[0])
        except ClientDisconected as my_except:
            print(my_except)
            self._clients.remove(sender)
        except BadRequestFromClientError:
            sender.send(self.protocol.bad_resp(400))
        except AttributeError:
            sender.send(self.protocol.bad_resp(400))


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
    server.main_loop()
