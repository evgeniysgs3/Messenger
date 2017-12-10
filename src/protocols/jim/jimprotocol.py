import json
import time

from src.protocols.jim.errors import NoRequiredParameterActionError, MaxMsgLengthExceedError


def serialize_data(func):
    def decorated(*args, **kwargs):
        data = func(*args, **kwargs)
        if data.get("action") is None:
            raise NoRequiredParameterActionError
        elif len(data) > 501:
            raise MaxMsgLengthExceedError(args[0].user_name)
        ser_data = json.dumps(data).encode("utf-8")
        return ser_data
    return decorated

def serialize_data_server(func):
    def decorated(*args, **kwargs):
        data = func(*args, **kwargs)
        if len(data) > 501:
            raise MaxMsgLengthExceedError(args[0].user_name)
        ser_data = json.dumps(data).encode("utf-8")
        return ser_data
    return decorated


class JIMMsg:
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return "NEW_MSG:<{}>:FROM:{}=>{}".format(
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.msg.get('time'))),
            self.msg.get('from'), self.msg.get('message'))

class JIMProtocolClient:
    def __init__(self, user_name):
        self.user_name = user_name

    @serialize_data
    def presence_msg(self):
        presence_msg = {
            "action": "presence",
            "time": int(time.time()),
            "type": "status",
            "user": {
                "account_name": self.user_name,
                "status": "online"
            }
        }
        return presence_msg

    @serialize_data
    def add_contact_msg(self, user_name, contact_name):
        add_contact_msg = {
            "action": "add_contact",
            "user_name": user_name,
            "contact_name": contact_name,
            "time": int(time.time())
        }
        return add_contact_msg

    @serialize_data
    def get_contact_msg(self, user_name):
        get_contact_msg = {
            "action": "get_contact",
            "user": user_name,
            "time": int(time.time())
        }
        return get_contact_msg

    @serialize_data
    def contact_msg(self, msg, contact_name):
        msg_protocol = {
            "action": "msg",
            "time": int(time.time()),
            "to": str(contact_name),
            "from": str(self.user_name),
            "encoding": "utf-8",
            "message": msg
        }
        return msg_protocol

    @serialize_data
    def quit_msg(self):
        disconnect_msg = {
            "action": "quit",
            "time": int(time.time())
        }
        return disconnect_msg

    @serialize_data
    def authenticate_msg(self, password):
        authenticate_msg = {
            "action": "authenticate",
            "time": int(time.time()),
            "user": {
                "account_name": str(self.user_name),
                "password": str(password)
            }
        }
        return authenticate_msg

    @serialize_data
    def join_chat_msg(self, chat_name):
        join_chat = {
            "action": "leave",
            "time": int(time.time()),
            "room": str("#" + chat_name)
        }
        return join_chat

    @serialize_data
    def leave_chat_msg(self, chat_name):
        leave_chat_msg = {
            "action": "leave",
            "time": int(time.time()),
            "room": str("#" + chat_name)
        }
        return leave_chat_msg


class JIMProtocolServer:

    def __init__(self):
        pass

    @serialize_data_server
    def good_resp(self):
        good_resp = {
            "response": 200,
            "time": int(time.time()),
            "alert": "OK"
        }
        return good_resp

    # Выбрал такую струтуру ответа,
    # так как в ответе сервера должено быть обязательное поле response
    @serialize_data_server
    def count_contacts_resp(self, count_contacts, contact_list):
        count_contact = {
            "response": 202,
            "quantity": count_contacts,
            "contacts": contact_list
        }
        return count_contact

    @serialize_data_server
    def bad_resp(self, code):
        bad_resp_msg = {
            "response": code,
            "time": int(time.time()),
            "error": "Bad request"
        }
        return bad_resp_msg