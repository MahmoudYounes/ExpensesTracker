# TODO: verify that the category and currency ids belong to the same user
from flask import request

from datetime import datetime

from Models import RecordModel, AccountModel
from Utilities import * 
from server import db

class RecordController():
    def __init__(self, db):
        self._db = db

    def CreateRecordFromDTO(self, recordDto):
        newRecord = ConstructObjectModelFromDTO(RecordModel, recordDto)
        newRecord.UserId = request.user
        newRecord.PaymentDate = datetime.strptime(newRecord.PaymentDate.replace('-', '/'), "%Y/%m/%d")
        newRecord.CreatedAt = datetime.utcnow()
        newRecord.IsDeleted = False
        
        newRecord.PaymentCurrencyId = recordDto.PaymentCurrency['Id']
        newRecord.CategoryId = recordDto.PaymentCategory['Id']

        self._db.session.add(newRecord)
        try:
            self._db.session.flush()
            self._db.session.commit()
        except Exception as e:
            print(e)
            self._db.session.rollback()
            return False
        return newRecord.ExpensesId

    def GetAccountRecords(self, accountId):
        allRecords = RecordModel.query.filter_by(UserId=accountId).all()
        return allRecords

    def GetRecordInfo(self, recordId, accountId):
        record = RecordModel.query.filter_by(ExpensesId=recordId, UserId=accountId).first()
        if not record:
            return None
        return ConstructDTOFromObjectModel(RecordDTO, record)

    def DeleteRecord(self, recordId, accountId):
        record = RecordModel.query.filter_by(ExpensesId=recordId, UserId=accountId).first()
        if record == None:
            return False
        self._db.session.delete(record)
        self._db.session.commit() 
        return True
    
    def UpdateRecord(self, userId, **recordData):
        recordId = recordData.get('Id', None)
        if not recordId:
            raise ValueError("Id can't be empty")
        record = RecordModel.query.filter_by(ExpensesId=recordId).first()
        if not record:
            raise LookupError("No record found with this Id")
        if userId != record.UserId:
            raise Exception("Not your record to update -_-!")
        paymentValue = recordData.get("PaymentValue", None)
        paymentReason = recordData.get("PaymentReason", None)
        paymentDate = recordData.get("PaymentDate", None)

        if paymentValue:
            record.PaymentValue = paymentValue
        if paymentDate:
            record.PaymentDate = paymentDate
        if paymentReason:
            record.PaymentReason = paymentReason
        
        self._db.session.commit()

        return True
        
        

# DTOs must be deprecated
class RecordDTO():
    targets = ['ExpensesId', 'PaymentDate', 'PaymentReason', 'PaymentValue', 'PaymentCurrency', 'PaymentCategory', 'UserId', 'CreatedAt', 'IsIncome']
    required = ['PaymentDate', 'PaymentReason', 'PaymentValue', 'PaymentCurrency', 'PaymentCategory', 'IsIncome']

    def __init__(self, **jsonObj):
        for req in self.__class__.required:
            setattr(self, req, jsonObj.get(req, None))

    def IsValid(self):
        for req in self.required:
            if getattr(self, req) == None:
                return False
        return True

    