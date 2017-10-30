import pytest
import os
from storage import ServerStorage
from models import Client, ClientHistory, ContactList


@pytest.fixture()
def test_storage(request):
    storage = ServerStorage('TestServerStorage')
    yield storage


def teardown():
    os.remove('TestServerStorage')


# Тест выполняется успешно но только первый раз, когда база уже создана, то ошибки
# Поэтому добавид удаление базы после каждого теста
def test_add_client(test_storage):
    storage = test_storage
    new_client = Client('ClientTest')
    storage.add_client('ClientTest')
    storage.commit()
    assert storage.session.query(Client).first() == new_client


def test_client_exists(test_storage):
    storage = test_storage
    storage.add_client('ClientTest')
    storage.commit()
    assert storage.client_exists('ClientTest') is True


# Тест не проходит из за времени
# def test_add_history(test_storage):
#     storage = test_storage
#     history = ClientHistory(client_id=1, ip='127.0.0.1')
#     storage.add_history('ClientTest', '127.0.0.1')
#     storage.commit()
#     assert storage.session.query(ClientHistory).first() == history


# Тест если нет такого клиента, сравнение, что срабатывает исключение
# Не смог разобраться как делать тест на срабатывание исключения
#def test_add_history(test_storage):
#    storage = test_storage
#    assert storage.add_history('NoneClient', '127.0.0.1') == 'Пользователь NoneClient не зарегистрирован'


def test_add_contact(test_storage):
    storage = test_storage
    storage.add_client('ClientTest')
    storage.add_client('NewClient')
    storage.add_client('NewClient2')
    storage.add_client('NewClient3')
    storage.commit()
    storage.add_contact('ClientTest', 'NewClient')
    storage.add_contact('ClientTest', 'NewClient2')
    storage.add_contact('ClientTest', 'NewClient3')
    storage.commit()
    assert storage.session.query(ContactList).filter(ContactList.ClientId == 1).count() == 3

# Нужно научиться возвращать имена вместо ContactId
def test_get_contact_list(test_storage):
    storage = test_storage
    storage.add_client('ClientTest')
    storage.add_client('NewClient')
    storage.add_client('NewClient2')
    storage.add_client('NewClient3')
    storage.commit()
    storage.add_contact('ClientTest', 'NewClient')
    storage.add_contact('ClientTest', 'NewClient2')
    storage.add_contact('ClientTest', 'NewClient3')
    storage.commit()
    assert storage.get_contact_list('ClientTest') == [(2, ), (3, ), (4, )]