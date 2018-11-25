from server import db

class TokenModel(db.Model):
    __tablename__ = "expenses_tracker_token"
    Id = db.Column("Id", db.Integer, primary_key=True)
    Token = db.Column("Token", db.String(length=100))
    UserId = db.Column("UserId", db.ForeignKey("expenses_tracker_account.id"))
    CreationDate = db.Column("CreationDate", db.DateTime())
    TimeToLive = db.Column("TimeToLive", db.Integer)

    