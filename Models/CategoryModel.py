from server import db
from datetime import datetime
class CategoryModel(db.Model):
    __tablename__ = "expenses_tracker_category"

    CategoryId = db.Column("CategoryId", db.Integer, primary_key=True, autoincrement=True, nullable=False)
    CategoryName = db.Column("CategoryName", db.String(length=100))
    CreatedAt = db.Column("CreatedAt", db.DateTime)
    IsDeleted = db.Column("IsDeleted", db.Boolean)
    UserId = db.Column("UserId", db.ForeignKey("expenses_tracker_account.id"), nullable=False)

    def __init__(self, **kwargs):
        self.CategoryName = kwargs.get('CategoryName', None)
        self.UserId = kwargs.get('UserId', None)
        self.CreatedAt = datetime.utcnow()
        self.IsDeleted = False

    def __serialize__(self):
        retDict = {}
        retDict['Id'] = int(self.CategoryId)
        retDict['CategoryName'] = str(self.CategoryName)
        retDict['UserId'] = int(self.UserId)
        return retDict