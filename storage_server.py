from sqlalchemy import create_engine
from sqlalchemy.orm import mapper
from sqlalchemy import Table, Column, Integer, String, MetaData, Time, ForeignKey
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///StorageServer.sqlite', echo=False)
metadata = MetaData()
client_table = Table('client', metadata,
Column('id', Integer, primary_key=True),
Column('login', String),
Column('information', String))

client_history_table = Table('client_history', metadata,
Column('id', Integer, primary_key=True),
Column('id_client', Integer, ForeignKey('client.id')),
Column('entry_time', Time),
Column('ip_address', String))

# Не создавалась таблица без id
contact_list_table = Table('contact_list', metadata,
Column('id', Integer, primary_key=True),
Column('id_owner', Integer, ForeignKey('client.id')),
Column('id_client', Integer, ForeignKey('client.id')))

# Выполним запрос CREATE TABLE
metadata.create_all(engine)


# Создадим класс для отображения таблицы БД
class Client:
    def __init__(self, login, information):
        self.login = login
        self.information = information

    def __repr__(self):
       return "<Client('%s','%s')>" % (self.login, self.information)


class ClientHistory:
    def __init__(self, id_client, entry_time, ip_address):
        self.id_client = id_client
        self.entry_time = entry_time
        self.ip_address = ip_address

    def __repr__(self):
        return "<ClientHistory('%d','%s', '%s')>" % (
            self.id_client, self.entry_time, self.ip_address)


class ContactList:
    def __init__(self, id_owner, id_client):
        self.id_owner = id_owner
        self.id_client = id_client


def get_contact_list_by_id_owner(session, id_owner):
    print(' -- Список контактов для id: {} --'.format(id_owner))
    for contact in session.query(ContactList).filter(ContactList.id_owner == id_owner):
        print('-- {}'.format(contact))


# Выполним связывание таблицы и класса-отображения
m = mapper(Client, client_table)
print('Classic Mapping. Mapper: ', m)
m = mapper(ClientHistory, client_history_table)
print('Classic Mapping. Mapper: ', m)
m = mapper(ContactList, contact_list_table)


# Создадим объект-пользователя
classic_user1 = Client("Вася", "Василий Литвинов")
classic_user2 = Client("Петя", "Петя Морозов")
classic_user3 = Client("Валя", "Валя Тарасова")
classic_user4 = Client("Костя", "Костя Токарев")
classic_user5 = Client("Нина", "Нина Захарова")

Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()

# session.add_all(classic_user1,
#                 classic_user2,
#                 classic_user3,
#                 classic_user4,
#                 classic_user5)
# session.commit()

# print(session.query(Client.id).filter(Client.login == 'Вася').all())
