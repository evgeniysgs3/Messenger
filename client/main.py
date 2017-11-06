import argparse
import json
import logging
import sys
# Костыль, который нужно убрать не понимаю почему когда из консоли стартую
# main.py -w получаю ImportError client Not found
sys.path.append('/home/leming/Documents/PycharmProject/Messenger')
import os
from socket import *
from client.error.error import UsernameToLongError, MandatoryKeyError, ServerAvailabilityError
from config.constants import LOG_DIR
from log.decorators import Log
from log.log_config import setup_logger
from protocols.jim.jimprotocol import JIMProtocolClient

MAX_DATA_RECEIVE = 1024

# Устанавливаем клиентский логер
setup_logger('client', os.path.join(LOG_DIR, 'client.log'))
client_logger = logging.getLogger('client')
log = Log(client_logger)


class Client:

    def __init__(self):
        self._account_name = input("Введите имя клиента:")
        self.sock = None
        self.protocol = JIMProtocolClient(self._account_name)

    @property
    def account_name(self):
        """Имя клиента"""
        return self._account_name

    @account_name.setter
    def account_name(self, account_name_value):
        if len(account_name_value) > 26:
            raise UsernameToLongError(account_name_value)
        self._account_name = account_name_value

    @log
    def connect_to_server(self, addr, port):
        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect((addr, port))
            return self.sock
        except OSError:
            raise ServerAvailabilityError(addr, port)
        except ServerAvailabilityError:
            return -1

    @log
    def disconnect_server(self):
        """Послать quit_msg"""
        try:
            self.sock.send(self.protocol.quit_msg())
            self.sock.close()
        except OSError as disconnect_server_error:
            print("Ошибка отключения от сервера {}".format(
                disconnect_server_error)
            )

    @log
    def send_presence_msg(self):
        try:
            self.sock.send(self.protocol.presence_msg())
        except OSError as socket_send_msg_error:
            client_logger.warning("Ошибка отправки сообщения на сервер: {}".format(
                socket_send_msg_error)
            )

    @log
    def get_msg_from_chat(self):
        data = self.sock.recv(1024)
        print("Data from chat {}".format(data.decode("utf-8")))

    @log
    def send_chat_msg(self, chat_msg, chat_name):
        self.sock.send(self.protocol.chat_msg(chat_msg, chat_name))
        client_logger.info("Клиент <{}> отправил 'msg' сообщение серверу".format(
            self.account_name)
        )

    def add_contact(self, contact_name):
        self.sock.send(self.protocol.add_contact_msg(self._account_name, contact_name))

    @log
    def receive_response_from_server(self):
        try:
            data = self.sock.recv(MAX_DATA_RECEIVE)
        except OSError as socket_receive_msg_error:
            client_logger.warning("Ошибка при получении ответа от сервера: {}".format(
                socket_receive_msg_error)
            )
        unserialized_data = json.loads(data.decode("utf-8"))
        self.parse_data_from_server(unserialized_data)

    @log
    def parse_data_from_server(self, unserialized_data):
        if 'response' not in unserialized_data:
            raise MandatoryKeyError('response')
        elif unserialized_data.get('response') == 200:
            client_logger.info("Клиент <{}> получил ответ от сервера, статус: {}".format(
                self.account_name, unserialized_data.get('alert')
            ))
        elif unserialized_data.get('response') == 202:
            print("В списке контактов содержится: %s записей\n" % unserialized_data.get('quantity'))
            print("Список контактов %s" % unserialized_data.get('contacts'))
        elif unserialized_data.get('response') == 400:
            print("Не удачный запрос к серверу ошибка: {}. Повторите запрос.".format(
                unserialized_data.get('error')
            ))


def create_parser():
    parser = argparse.ArgumentParser(
        prog='client',
        description=
        """
        Клиентская часть мессенджера.
        """,
        epilog=
        """
        (c) September 2017.
        """)
    parser.add_argument(
        '-p', '--port', type=int, default=7777, help="""
        Порт на котором работает сервер""")
    parser.add_argument(
        '-a', '--addr', default='127.0.0.1', help="""
        IP-адрес для подключения к серверу.
        """)
    parser.add_argument('-r', action='store_const', const=True, help="""
        Клиент запущен в режиме чтения чата
        """)
    parser.add_argument('-w', action='store_const', const=True, help="""
        Клиент запущен в режиме передачи сообщений в чат
        """)
    return parser


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    addr = namespace.addr
    port = namespace.port
    client = Client()
    c = client.connect_to_server(addr, port)
    client.send_presence_msg()
    data_from_server = c.recv(1024)
    print(data_from_server)
    if namespace.r:
        print("Клиент <{}> запущен в режиме чтения чата".format(client.account_name))
        while True:
            client.get_msg_from_chat()
    elif namespace.w:
        while True:
            msg = input("""1. Добавить контакт (add name);\n2. Получить списко контактов (get);\n3. Выйти(q);\nВведите групповое сообщение или команду:> """)
            if msg == 'q':
                # Не работает, сразу вешает сервак, видимо из-за subprocess
                client.disconnect_server()
            elif msg.startswith('add'):
                contact_name = msg.split()[1]
                client.add_contact(contact_name)
            else:
                client.send_chat_msg(msg, 'room')
    else:
        while True:
            client.receive_response_from_server()
    client.disconnect_server()
