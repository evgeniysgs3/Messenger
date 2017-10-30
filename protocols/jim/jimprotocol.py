import json
import time

from protocols.jim.error.error import NoRequiredParameterActionError, MaxMsgLengthExceedError


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
    def chat_msg(self, msg, chat_name):
        msg_protocol = {
            "action": "msg",
            "time": int(time.time()),
            "to": str("#" + chat_name),
            "from": str(self.user_name),
            "encoding": "utf-8",
            "message": msg
        }
        return msg_protocol

    @serialize_data
    def quit_msg(self):
        disconnect_msg = {
            "action": "quit"
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

    def send_response(self):
        pass