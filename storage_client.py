import os
from sqlalchemy import create_engine
from sqlalchemy.orm import mapper
from sqlalchemy import Table, Column, Integer, String, MetaData, Time, ForeignKey
from sqlalchemy.orm import sessionmaker

f_storage_client = os.path.join(os.path.abspath('.'), 'StorageClient.sqlite')

engine = create_engine('sqlite:///StorageClient.sqlite', echo=False)
metadata = MetaData()
contact_list_table = Table('contact_list', metadata,
Column('id', Integer, primary_key=True),
Column('contact_name', String),
Column('contact_inf', String))

message_history_table = Table('message_history', metadata,
Column('id', Integer, primary_key=True),
Column('id_contact', Integer, ForeignKey('contact_list.id')),
Column('message', String))

# Выполним запрос CREATE TABLE
metadata.create_all(engine)


# Создадим класс для отображения таблицы БД
class ContactList:
    def __init__(self, contact_name, contact_inf):
        self.contact_name = contact_name
        self.contact_inf = contact_inf


class MessageHistory:
    def __init__(self, id_contact, message):
        self.id_contact = id_contact
        self.message = message


def get_contact_list_by_id_owner(session, id_owner):
    print(' -- Список контактов для id: {} --'.format(id_owner))
    for contact in session.query(ContactList).filter(ContactList.id_owner == id_owner):
        print('-- {}'.format(contact))


# Выполним связывание таблицы и класса-отображения
m = mapper(ContactList, contact_list_table)
print('Classic Mapping. Mapper: ', m)
m = mapper(MessageHistory, message_history_table)
print('Classic Mapping. Mapper: ', m)

Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()

# print(session.query(Client.id).filter(Client.login == 'Вася').all())
