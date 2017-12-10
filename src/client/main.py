import os
import sys
import argparse
import json
import logging
import threading
from queue import Queue
from socket import *

from PyQt5.QtCore import pyqtSignal, QObject
from src.client.errors import UsernameToLongError, MandatoryKeyError, ServerAvailabilityError
from src.log.log_config import setup_logger
from src.protocols.jim.jimprotocol import JIMProtocolClient, JIMMsg
from src.config.constants import LOG_DIR

from src.log.decorators import Log

MAX_DATA_RECEIVE = 1024

# Устанавливаем клиентский логер
setup_logger('client', os.path.join(LOG_DIR, 'client.log'))
client_logger = logging.getLogger('client')
log = Log(client_logger)
menu_for_console_client = """
1. Добавить контакт (add name);
2. Получить списко контактов (get);
3. Ввод сообщения контакту (contact_name msg);
4. Выйти(q);
"""

class Receiver:

    def __init__(self, socket, queue_msg, client):
        self.sock = socket
        self.queue_in_messages = queue_msg
        self.client = client
        self.is_alive = False

    def __call__(self):
        self.is_alive = True
        while self.is_alive:
            serialized_data = self.sock.recv(MAX_DATA_RECEIVE)
            if serialized_data:
                try:
                    self.parse_data_from_server(serialized_data)
                # Если это не ответ сервера, то выводим на экран
                except MandatoryKeyError:
                    data = json.loads(serialized_data.decode("utf-8"))
                    msg = JIMMsg(data)
                    self.process_message(str(msg))
                    # Добавляем signal для вывода сообщений в форму
                    print(menu_for_console_client)
            else:
                break

    def process_message(self, data):
        pass

    def stop(self):
        self.is_alive = False

    @log
    def parse_data_from_server(self, serialized_data):
        data = json.loads(serialized_data.decode("utf-8"))
        if 'response' not in data:
            raise MandatoryKeyError('response')
        else:
            self.queue_in_messages.put(data)

class GuiReceiver(Receiver, QObject):
    gotMsg = pyqtSignal(str)
    finished = pyqtSignal(int)

    def __init__(self, sock, request_queue, client):
        Receiver.__init__(self, sock, request_queue, client)
        QObject.__init__(self)

    def process_message(self, data):
        self.gotMsg.emit(data)

    def poll(self):
        super().poll()
        self.finished.emit(0)

class Client:

    def __init__(self, login):
        #self._account_name = input("Введите имя клиента:")
        self._account_name = login
        self.sock = None
        self.protocol = JIMProtocolClient(self._account_name)
        self.queue_in_messages = Queue()
        self.listener = None

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
            return 1
        except OSError:
            raise ServerAvailabilityError(addr, port)
        except ServerAvailabilityError:
            return 0

    @log
    def disconnect_server(self):
        """Послать quit_msg"""
        try:
            self.sock.send(self.protocol.quit_msg())
        except OSError as disconnect_server_error:
            print("Ошибка отключения от сервера {}".format(
                disconnect_server_error)
            )

    @log
    def send_presence_msg(self):
        try:
            self.sock.send(self.protocol.presence_msg())
            response_srv = self.queue_in_messages.get()
            if response_srv.get('response') == 200:
                print("Мы успешно подключились к серверу.")
        except OSError as socket_send_msg_error:
            client_logger.warning("Ошибка отправки сообщения на сервер: {}".format(
                socket_send_msg_error)
            )

    @log
    def get_msg_from_chat(self):
        data = self.sock.recv(MAX_DATA_RECEIVE)
        print("Data from chat {}".format(data.decode("utf-8")))

    @log
    def send_contact_msg(self, chat_msg, contact_name):
        self.sock.send(self.protocol.contact_msg(chat_msg, contact_name))

    def add_contact(self, contact_name):
        self.sock.send(self.protocol.add_contact_msg(self._account_name, contact_name))
        response_server = self.queue_in_messages.get()
        print(response_server)
        if response_server.get('response') == 200:
            print("Контакт {} успешно добавлен.".format(contact_name))

    def get_contact_list(self):
        self.sock.send(self.protocol.get_contact_msg(self._account_name))
        data = self.queue_in_messages.get()
        if data.get('response') == 202:
            print("В списке контактов содержится: %s записей\n" % data.get('quantity'))
            print("Список контактов %s" % data.get('contacts'))

    def get_contact_list_gui(self):
        """Возвращает количество контактов и их список"""

        self.sock.send(self.protocol.get_contact_msg(self._account_name))
        data = self.queue_in_messages.get()
        if data.get('response') == 202:
            return data.get('quantity'), data.get('contacts')

    def start_gui_client(self, addr, port):
        if not self.connect_to_server(addr, port):
            print("Сервер не доступен!")
            sys.exit()
        self.listener = GuiReceiver(self.sock, self.queue_in_messages, self)
        th_listen = threading.Thread(target=self.listener)
        th_listen.daemon = True
        th_listen.start()
        # Посылаем приветственое сообщение серверу


        self.send_presence_msg()

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
    client = Client('qaz')
    if not client.connect_to_server(addr, port):
        print("Сервер не доступен!")
        sys.exit()
    listener = Receiver(client.sock, client.queue_in_messages, client)
    th_listen = threading.Thread(target=listener)
    th_listen.daemon = True
    th_listen.start()
    # Посылаем приветственое сообщение серверу
    client.send_presence_msg()
    while True:
        print(menu_for_console_client)
        msg = input(":>")
        if msg == 'q':
            # Не работает, сразу вешает сервак, видимо из-за subprocess
            client.disconnect_server()
        elif msg.startswith('add'):
            contact_name = msg.split()[1]
            client.add_contact(contact_name)
        elif msg.startswith('get'):
            client.get_contact_list()
        else:
            client.send_contact_msg(' '.join(msg.split()[1:]), msg.split()[0])