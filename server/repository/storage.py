from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import ClientHistory, Client, ContactList, Base
from errors import NoneClientError


class ServerStorage:

    def __init__(self, name):
        self.name = name
        engine = create_engine('sqlite:///{}'.format(self.name), echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()
        self.session = session
        # сначала будем всегда пересоздавать базу
        self._create_database(engine)

    def commit(self):
        self.session.commit()

    def rolback(self):
        self.session.rolback()

    def _create_database(self, engine):
        Base.metadata.create_all(engine)

    def add_client(self, username, info=None):
        new_item = Client(username, info)
        self.session.add(new_item)

    def client_exists(self, username):
        result = self.session.query(Client).filter(Client.Name == username).count() > 0
        return result

    def _get_client_by_username(self, username):
        client = self.session.query(Client).filter(Client.Name == username).first()
        return client

    def add_history(self, username, ip):
        client = self._get_client_by_username(username)
        if client:
            history = ClientHistory(client_id=client.ClientId, ip=ip)
            self.session.add(history)
        else:
            raise NoneClientError(username)

    def add_contact(self, client_username, contact_username):
        client = self._get_client_by_username(client_username)
        if client:
            contact = self._get_client_by_username(contact_username)
            if contact:
                contact_list = ContactList(client_id=client.ClientId, contact_id=contact.ClientId)
                self.session.add(contact_list)
            else:
                raise NoneClientError(contact_username)
        else:
            raise NoneClientError(client_username)

    def get_contact_list(self, user_name):
        client = self._get_client_by_username(user_name)
        if client:
            contact_list = self.session.query(ContactList.ContactId).filter(ContactList.ClientId == client.ClientId).all()
            return contact_list
        else:
            raise NoneClientError(user_name)