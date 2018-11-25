from server import db
from Utilities import * 
class RecordModel(db.Model):
    __tablename__ = 'expenses_tracker_record'
    
    ExpensesId = db.Column('ExpensesId', db.Integer, primary_key=True)
    PaymentDate = db.Column('PaymentDate', db.Date)
    PaymentReason = db.Column('PaymentReason', db.String(length=300))
    PaymentValue = db.Column('PaymentValue', db.Integer)
    PaymentCurrencyId = db.Column('PaymentCurrency_id', db.ForeignKey('expenses_tracker_currency.CurrencyId'), nullable=False)
    CategoryId = db.Column('CategoryId_Id', db.ForeignKey('expenses_tracker_category.CategoryId'), nullable=False) 
    UserId = db.Column('UserId_Id', db.ForeignKey('expenses_tracker_account.id'), nullable=False)
    CreatedAt = db.Column('CreatedAt', db.DateTime())
    IsDeleted = db.Column('IsDeleted', db.Boolean, default=False)
    IsIncome = db.Column('IsIncome', db.Boolean, default=False)

    currency = db.relationship('CurrencyModel', backref='CurrencyModel')
    category = db.relationship('CategoryModel', backref='CategoryModel')


    def __serialize__(self):
        retDict = {}
        retDict['Id'] = str(int(self.ExpensesId))
        retDict['PaymentDate'] = SerializeDate(self.PaymentDate)
        retDict['PaymentReason'] = str(self.PaymentReason)
        retDict['PaymentValue'] = str(int(self.PaymentValue))
        retDict['PaymentCurrency'] = self.currency.__serialize__()
        retDict['PaymentCategory'] = self.category.__serialize__()
        retDict['UserId'] = int(self.UserId)
        retDict['IsIncome'] = True if self.IsIncome else False
        return retDict