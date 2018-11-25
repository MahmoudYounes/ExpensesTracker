from server import db
from datetime import datetime

class CurrencyModel(db.Model):
    __tablename__ = "expenses_tracker_currency"

    CurrencyId = db.Column("CurrencyId", db.Integer, primary_key=True)
    CreatedAt = db.Column("CreatedAt", db.DateTime)
    CurrencyName = db.Column("CurrencyName", db.String(length=100))
    CurrencySlug = db.Column("CurrencySlug", db.String(length=100))
    IsDeleted = db.Column("IsDeleted", db.Boolean)
    UserId = db.Column("UserId", db.ForeignKey("expenses_tracker_account.id"))
    
    def __init__(self, **kwargs):
        self.CurrencyName = kwargs.get('CurrencyName', None)
        self.CurrencySlug = kwargs.get('CurrencySlug', None)
        self.UserId = kwargs.get('UserId', None)
        self.CreatedAt = datetime.utcnow()
        self.IsDeleted = False

    def __serialize__(self):
        retDict = {}
        retDict['Id'] = int(self.CurrencyId)
        retDict['CurrencyName'] = str(self.CurrencyName)
        retDict['CurrencySlug'] = str(self.CurrencySlug)
        retDict['UserId'] = self.UserId
        return retDict