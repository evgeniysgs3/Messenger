import json
import sys
import time
from socket import *

MAX_DATA_RECEIVE = 1024


class Client:

    def __init__(self, ip='127.0.0.1', port=8080):
        self.account_name = input("Введите имя пользователя:")
        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect((ip, port))
        except OSError as socket_connect_error:
            print("Ошибка подключения к серверу: {}".format(
                socket_connect_error)
            )
            sys.exit(1)

    def send_presence_msg(self):
        presence_msg = {
                "action": "presence",
                "time": int(time.time()),
                "type": "status",
                "user": {
                    "account_name": self.account_name,
                    "status": "Yep, I am here!"
                }
            }
        serialized_presence_msg = json.dumps(presence_msg).encode("utf-8")
        try:
            self.sock.send(serialized_presence_msg)
        except OSError as socket_send_msg_error:
            print("Ошибка отправки сообщения на сервер: {}".format(
                socket_send_msg_error)
            )

    def receive_response_from_server(self):
        try:
            data = self.sock.recv(MAX_DATA_RECEIVE)
        except OSError as socket_receive_msg_error:
            print("Ошибка при получении ответа от сервера: {}".format(
                socket_receive_msg_error)
            )
        unserialized_data = json.loads(data.decode("utf-8"))
        self.parse_data_from_server(unserialized_data)

    def parse_data_from_server(self, unserialized_data):
        if unserialized_data['response'] == 200:
            print("Клиент <{}> успешно подключился к серверу, статус: {}".format(
                self.account_name, unserialized_data['alert']
            ))
        elif unserialized_data['response'] == 400:
            print("Не удачный запрос к серверу ошибка: {}. Повторите запрос.".format(
                unserialized_data['error']
            ))

client = Client()
client.send_presence_msg()
client.receive_response_from_server()
