import json
import sys
import time
from socket import *

MAX_DATA_RECEIVE = 1024
MAX_CLIENT_CONNECTION = 10


class Server:

    def __init__(self, port=8080):
        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.bind(('', port))
            self.sock.listen(MAX_CLIENT_CONNECTION)
        except OSError as start_server_error:
            print("Ошибка при запуске сервера: {}".format(start_server_error))
            sys.exit(1)

    def start(self):
        while True:
            client, addr = self.sock.accept()
            data = client.recv(MAX_DATA_RECEIVE)
            self.parse_data_from_clietn(client, addr, data)

    def parse_data_from_clietn(self, client, addr, data):
        try:
            unserialized_data = json.loads(data.decode("utf-8"))
            account_name = unserialized_data['user']['account_name']
            if unserialized_data['action'].startswith('presence'):

                print("Клиент {} подключился к серверу с IP: {} <{}>".format(
                    account_name, addr[0], unserialized_data['time'])
                )
                self.send_good_response_to_client(client, 200, account_name)
            else:
                raise Exception("Ошибка при чтении данных от клиента {}".format(
                    account_name))
        except Exception as err:
            self.send_bad_response_to_client(client, 400, account_name)
            print("Отпраляем клиенту сведения об ошибке сервера. {}".format(err))

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


server = Server()
server.start()
