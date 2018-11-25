# working on this when needed right now not needed

from Models import TokenModel

from datetime import datetime

class TokenController:
    def GetToken(self, userEmail):
         token = jwt.encode({
            'email': email,
            'exp'  : datetime.utcnow() + timedelta(minutes=600)
            }, app.config.get('SECRET_KEY', 'SECRET_PRECIOUIS_KEY'))
