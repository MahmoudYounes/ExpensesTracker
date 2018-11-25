from flask import request, g
from datetime import datetime, timedelta
import jwt

from Models import CurrencyModel
from Utilities.Utilities import *

from server import app, db
from Utilities import *


class CurrencyController:

    required = ['UserId', 'CurrencyName', 'CurrencySlug']

    def __init__(self, db):
        self._db = db

    def GetCurrencyBy(self, Id=None):
        targetCurrency = None
        if Id:
            targetCurrency = CurrencyModel.query.filter_by(Id=Id).first()
        if targetCurrency and not targetCurrency.IsDeleted:
            return targetCurrency
        else:
            return None
    
    def CreateCurrencyFromDTO(self, jsonObj):
        if not IsValid(jsonObj, self.__class__.required):
            return None

        duplicateCurrency = CurrencyModel.query.filter_by(CurrencyName=jsonObj.CurrencyName, CurrencySlug=jsonObj.CurrencySlug, UserId=request.user).first()
        if duplicateCurrency:
            raise ValueError("There already exists a Currency with the same name.")
        
        newCurrency = CurrencyModel(**jsonObj)
        self._db.session.add(newCurrency)
        try:
            self._db.session.flush()
            self._db.session.commit()
        except Exception as e:
            print(e)
            self._db.session.rollback()
            return False
        return newCurrency.CurrencyId

    def GetAllCurrencies(self):
        allCurrencies = CurrencyModel.query.all()
        return allCurrencies
    
    def GetAccountCurrencies(self, userId):
        allCurrencies = CurrencyModel.query.filter_by(UserId=userId).all()
        return allCurrencies
    
    def DeleteCurrency(self, id, userId):
        currency = CurrencyModel.query.filter_by(CurrencyId=id, UserId=userId).first()
        if currency == None:
            return False
        self._db.session.delete(currency)
        self._db.session.commit()
        return True


# will be deprecated
class CurrencyDTO:
    targets = ['CurrencyId', 'CurrencyName', 'CurrencySlug', 'CreatedAt', 'UserId']
    required = ['CurrencyName', 'CurrencySlug', 'UserId']
    def __init__(self, **kwargs):
        self.CurrencyName = kwargs.get('CurrencyName', None)
        self.CurrencySlug = kwargs.get('CurrencySlug', None)
        self.UserId = kwargs.get('UserId', None)

    def IsValid(self):
        for req in self.required:
            if getattr(self, req) == None:
                return False
        return True