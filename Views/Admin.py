from flask import Blueprint

from Controllers import AccountController
from wrappers import *
from server import db
from Utilities import *

adminBlueprint = Blueprint("adminBlueprint", __name__, url_prefix="/admin/account")
accountController = AccountController(db)


@adminBlueprint.route('/', methods=['GET'])
@adminBlueprint.route('/<accountId>')
@AuthorizedAdminUser
def RetrieveAllAccounts(accountId=None):
    if ValidateId(accountId):
        account = accountController.GetAccountBy(Id=accountId)
        return jsonify(account.Serialize())
    else:
        return jsonify(SerializeList(accountController.GetAllAccounts()))



@adminBlueprint.route('/<accountId>', methods=['DELETE'])
@AuthorizedAdminUser
def DeleteAccount(accountId):
    success = accountController.DeleteAccount(accountId)
    if success:
        return jsonify("account deleted"), 200
    return jsonify("failed to delete account"), 400