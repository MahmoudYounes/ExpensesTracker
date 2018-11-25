from flask import jsonify, Blueprint, request

from server import app, db
from wrappers import AuthorizedAdminUser, AuthenticatedUser
from Controllers.AccountController import AccountController

accountController = AccountController(db)
accountBlueprint = Blueprint('accountBlueprint', __name__, url_prefix='/account')


@accountBlueprint.route('/', methods=['GET'])
@AuthenticatedUser
def GetAccountInfo():
    user = accountController.GetAccountBy(Id=request.user)
    if user == None:
        return jsonify("user not found"), 404
    return jsonify(user.__serialize__(returnRecords=True))