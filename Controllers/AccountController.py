from flask import request, g
from datetime import datetime, timedelta
import jwt
import traceback
from Models import AccountModel
from Controllers.RecordController import RecordDTO
from Utilities.Utilities import IsValid

from server import app

from werkzeug.security import check_password_hash

# TODO: implement validate password in this controller
# TODO: implement expressive error handling scheme

class AccountController:
    
    required = ['username', 'email', 'password', 'firstName', 'lastName']

    def __init__(self, db):
        self._db = db
    
    def GetAccountBy(self, Id=None, email=None, username=None):
        if username:
            targetAccount = AccountModel.query.filter_by(username=username).first()
        if email:
            targetAccount = AccountModel.query.filter_by(email=email).first()
        if Id:
            targetAccount = AccountModel.query.filter_by(Id=Id).first()
        if targetAccount:
            return targetAccount
        else:
            return None
    
    def CreateAccountFromJson(self, jsonObj):
        duplicateAccount = AccountModel.query.filter_by(email=jsonObj.email).first()
        if duplicateAccount:
            raise ValueError("There already exists an account with the same email. please login with it.")
        
        if not IsValid(jsonObj, self.__class__.required):
            raise ValueError("Required fields do not exist. required fields are username, email, password, first name, last name")

        newUser = AccountModel(**jsonObj)
        self._db.session.add(newUser)
        try:
            self._db.session.flush()
            self._db.session.commit()
        except:
            self._db.session.rollback()
            return False
        return newUser.Id

    def GetAllAccounts(self):
        allAccounts = AccountModel.query.all()
        return allAccounts

    def GetUserToken(self, email, password):
        try:
            try:
                knownUser = AccountModel.query.filter_by(email=email).first()
            except Exception as e:
                traceback.print_exc()
                return
            if not knownUser or not check_password_hash(knownUser.password, password):
                return None
            token = jwt.encode({
                'email':knownUser.email,
                'exp'  :datetime.utcnow() + timedelta(minutes=600)
                }, app.config.get('SECRET_KEY', 'SECRET_PRECIOUIS_KEY'))
            return token

        except Exception as e:
            print(e)
            return None
    
    def InsertAccount(self, account):
        if not isinstance(account, AccountModel):
            return False
        
        self._db.add(account)
        self._db.session.flush()
        self._db.session.commit()
        return account.Id

    def DeleteAccount(self, accountId):
        accountToDelete = AccountModel.query.filter_by(Id=accountId).first()
        if not accountToDelete:
            return False
        self._db.session.delete(accountToDelete)
        self._db.session.commit()
        return True
    
# will be deprecated
class AccountDTO:
    targets = ['Id', 'lastLogin', 'isSuperUser', 'username', 'firstName', 'lastName', 'email', 'isStaff', 'isActive', 'dateJoined']
    required = ['username', 'email', 'password', 'firstName', 'lastName']
    def __init__(self, **kwargs):
        self.Id = kwargs.get('Id', None) 
        self.lastLogin = kwargs.get('lastLogin', None) 
        self.isSuperUser = kwargs.get('isSuperUser', None) 
        self.username = kwargs.get('username', None) 
        self.firstName = kwargs.get('firstName', None), 
        self.lastName = kwargs.get('lastName', None)
        self.password = kwargs.get('password', None)
        self.email = kwargs.get('email', None) 
        self.isStaff = kwargs.get('isStaff', None) 
        self.isActive = kwargs.get('isActive', None) 
        self.dateJoined = kwargs.get('dateJoined', None)
            
        




