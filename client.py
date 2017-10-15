import json
import sys
import argparse
import time
from socket import *
from jimprotocol import JIMProtocol
from errors import \
    UsernameToLongError, MandatoryKeyError,\
    MaxMsgLengthExceedError, ServerAvailabilityError,\
    NoRequiredParameterActionError


MAX_DATA_RECEIVE = 1024


class Client:

    def __init__(self):
        self._account_name = "TestReader"
        self.sock = None
        self.protocol = JIMProtocol(self._account_name)

    @property
    def account_name(self):
        """Имя клиента"""
        return self._account_name

    @account_name.setter
    def account_name(self, account_name_value):
        if len(account_name_value) > 26:
            raise UsernameToLongError(account_name_value)
        self._account_name = account_name_value

    def connect_to_server(self, addr, port):
        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect((addr, port))
            print("Клиент <{}> успешно подключился к серверу".format(
                self.account_name)
            )
            return self.sock
        except OSError:
            raise ServerAvailabilityError(addr, port)
        except ServerAvailabilityError:
            return -1

    def disconnect_server(self):
        """Послать quit_msg"""
        try:
            self.sock.close()
            print("Клиент <{}> отсоединен от сервера".format(
                self.account_name)
            )
        except OSError as disconnect_server_error:
            print("Ошибка отключения от сервера {}".format(
                disconnect_server_error)
            )

    def send_presence_msg(self):
        try:
            self.sock.send(self.protocol.presence_msg())
            print("Клиент <{}> отправил 'presence' сообщение серверу".format(
                self.account_name)
            )
            return 0
        except OSError as socket_send_msg_error:
            print("Ошибка отправки сообщения на сервер: {}".format(
                socket_send_msg_error)
            )
        except NoRequiredParameterActionError:
            return -1

    def get_msg_from_chat(self):
        data = self.sock.recv(1024)
        print("Data from chat {}".format(data.decode("utf-8")))

    def send_chat_msg(self, chat_msg, chat_name):
        try:
            if len(chat_msg) > 501:
                raise MaxMsgLengthExceedError(self.account_name)
            self.sock.send(self.protocol.chat_msg(chat_msg, chat_name))
            print("Клиент <{}> отправил 'msg' сообщение серверу".format(
                self.account_name)
            )
        except MaxMsgLengthExceedError:
            return -1
        except NoRequiredParameterActionError:
            return -1

    def receive_response_from_server(self):
        try:
            data = self.sock.recv(MAX_DATA_RECEIVE)
            print(data)
        except OSError as socket_receive_msg_error:
            print("Ошибка при получении ответа от сервера: {}".format(
                socket_receive_msg_error)
            )
        unserialized_data = json.loads(data.decode("utf-8"))
        self.parse_data_from_server(unserialized_data)

    def parse_data_from_server(self, unserialized_data):
        if 'response' not in unserialized_data:
            raise MandatoryKeyError('response')
        elif unserialized_data.get('response') == 200:
            print("Клиент <{}> получил ответ от сервера, статус: {}".format(
                self.account_name, unserialized_data.get('alert')
            ))
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
    if namespace.r:
        print("Клиент <{}> запущен в режиме чтения чата".format(client.account_name))
        while True:
            message = c.recv(1024)
            print(message.decode('utf-8'))
    elif namespace.w:
        while True:
            msg = input("Введите групповое сообщение:>")
            c.send(msg.encode("utf-8"))
    else:
        while True:
            client.receive_response_from_server()
    client.disconnect_server()
