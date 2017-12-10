import pytest
import server

from src import client


@pytest.fixture(scope='module')
def testserver(request):
    serv = server.Server('127.0.0.1', 7777)
    serv.start()

    def fin():
        serv.stop()
    request.addfinolized(fin)


def test_connect_to_server():
    c = client.Client()
    assert c.connect_to_server('127.0.0.1', 7777) is None


def test_send_presence_msg():
    c = client.Client()
    c.connect_to_server('127.0.0.1', 7777)
    assert c.send_presence_msg()


# здесь у меня тест не проходит, не понимаю по какой причине пока что((
def test_receive_response_from_server():
    c = client.Client()
    c.connect_to_server('127.0.0.1', 7777)
    c.send_presence_msg()
    assert c.receive_response_from_server()
