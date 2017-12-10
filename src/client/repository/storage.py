from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.client import NoneContactError
from .repository.modeles import Contact, Message


class ClientStorage:

    def __init__(self, name):
        self.name = name
        engine = create_engine('sqlite:///{}'.format(self.name), echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()
        self.session = session
        # пересоздаем базу
        self._create_database(engine)

    def add_contact(self, username):
        new_contact = Contact(username)
        self.session.add(new_contact)

    def _get_contact_by_username(self, username):
        contact = self.session.query(Contact).filter(Contact.Name == username).first()
        return contact

    def del_contact(self, username):
        contact = self._get_contact_by_username(username)
        self.session.delete(contact)

    def get_contacts(self):
        contacts = self.session.query(Contact)
        return contacts

    def add_message(self, username, text):
        contact = self._get_contact_by_username(username)
        if contact:
            new_message = Message(text=text, contact_id=contact.ContactId)
            self.session.add(new_message)
        else:
            raise NoneContactError(username)