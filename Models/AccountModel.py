# TODO: complete email validation
# TODO: add validations on password
# TODO: add validations on username
# TODO: mark important fields as nullable
from sqlalchemy.orm import validates
from server import db
from Utilities import *

from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class AccountModel(db.Model):
    __tablename__ = 'expenses_tracker_account'

    Id = db.Column('id', db.Integer, primary_key=True, nullable=False)
    password = db.Column('password', db.String(length=128, collation='latin1_swedish_ci'), nullable=False)
    lastLogin = db.Column('last_login', db.DateTime())
    isSuperUser = db.Column('is_superuser', db.Boolean)
    username = db.Column('username', db.String(length=150))
    firstName = db.Column('first_name', db.String(length=30, collation='latin1_swedish_ci'))
    lastName = db.Column('last_name', db.String(length=30, collation='latin1_swedish_ci'))
    email = db.Column('email', db.String(length=254, collation='latin1_swedish_ci'))
    isStaff = db.Column('is_staff', db.Boolean)
    isActive = db.Column('is_active', db.Boolean)
    dateJoined = db.Column('date_joined', db.DateTime)

    records = db.relationship("RecordModel", backref="RecordModel")

    def __init__(self, **kwargs):
        tpassword = kwargs.get('password', None)
        self.password = generate_password_hash(tpassword, 'sha256', salt_length=10) if tpassword != None else None
        self.isSuperUser = False
        self.username = kwargs.get('username', None)
        self.firstName = kwargs.get('firstName', None)
        self.lastName = kwargs.get('lastName', None)
        self.email = kwargs.get('email', None)
        self.isStaff = False
        self.isActive = True
        self.dateJoined = datetime.utcnow()

    def __serialize__(self, returnRecords=False):
        retDict = {}
        retDict['Id'] = int(self.Id)
        retDict['lastLogin'] = SerializeDate(self.lastLogin)
        retDict['isSuperUser'] = 'true' if self.isSuperUser else 'false'
        retDict['username'] = str(self.username)
        retDict['firstName'] = str(self.firstName)
        retDict['lastName'] = str(self.lastName)
        retDict['email'] = str(self.email)
        retDict['isStaff'] = 'true' if self.isStaff else 'false'
        if returnRecords:
            retDict['records'] = [record.__serialize__() for record in self.records]
        return retDict