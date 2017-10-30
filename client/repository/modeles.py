import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationships

Base = declarative_base()


class Contact(Base):
    __tablename__ = 'Contact'
    ContactId = Column(Integer, primary_key=True)
    Name = Column(String, unique=True)

    def __init__(self, name):
        self.Name = name

    def __repr__(self):
        return "<Contact ('%s')>" % self.Name

    def __eq__(self, other):
        return self.Name == other.Name


class Message(Base):
    __tablename__ = 'Message'
    MessageId = Column(Integer, primary_key=True)
    Text = Column(String)
    CreatedDatetime = Column(DateTime, default=datetime.datetime.utcnow)
    ContactId = Column(Integer, ForeignKey('Contact.ContactId'))
    Contact = relationships("Contact", back_populates="Messages")

    def __init__(self, text, contact_id, creation_datetime=None):
        self.Text = text
        self.ContactId = contact_id
        if creation_datetime:
            self.CreatedDatetime = creation_datetime

    def __repr__(self):
        return "<Message ('%s', %d)>" % (self.Text, self.ContactId)

    def __eq__(self, other):
        return self.Text == other.Text and \
               self.CreatedDatetime == other.CreatedDatetime and \
               self.ContactId == other.ContactId

Contact.Message = relationships("Message", order_by=Message.CreatedDatetime,
                                back_populates="Contact")