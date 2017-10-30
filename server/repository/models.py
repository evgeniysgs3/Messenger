import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class ContactList(Base):
    __tablename__ = 'ContactList'
    ContactListId = Column(Integer, primary_key=True)
    ClientId = Column(Integer, ForeignKey('Client.ClientId'))
    ContactId = Column(Integer, ForeignKey('Client.ClientId'))

    def __init__(self, client_id, contact_id):
        self.ContactId = contact_id
        self.ClientId = client_id


class Client(Base):
    __tablename__ = 'Client'
    ClientId = Column(Integer, primary_key=True)
    Name = Column(String, unique=True)
    Info = Column(String, nullable=True)

    def __init__(self, name, info=None):
        self.Name = name
        if info:
            self.Info = info

    def __repr__(self):
        return "<Client {}>".format(self.Name)

    def __eq__(self, other):
        return self.Name == other.Name


class ClientHistory(Base):
    __tablename__ = 'ClientHistory'
    ClientHistoryId = Column(Integer, primary_key=True)
    ClientId = Column(Integer, ForeignKey('Client.ClientId'))
    EntryTime = Column(DateTime, default=datetime.datetime.utcnow)
    IpAddress = Column(String)
    Client = relationship("Client", back_populates="ClientHistories")

    def __init__(self, client_id, ip, entry_time=None):
        self.IpAddress = ip
        self.ClientId = client_id
        if entry_time:
            self.EntryTime = entry_time

    def __repr__(self):
        return "<ClientHistory ('%s', %d)>" % (self.IpAddress, self.ClientId)

    def __eq__(self, other):
        return self.IpAddress == other.IpAddress and \
               self.EntryTime == other.EntryTime and \
               self.ClientId == other.ClientId

Client.ClientHistories = relationship("ClientHistory", order_by=ClientHistory.EntryTime, back_populates="Client")
contact = ContactList(1, 2)
print(contact)