from flask import jsonify, Blueprint, request

from server import db
from wrappers import *
from Controllers import CurrencyController, CurrencyDTO, AccountController
from Utilities import *


currencyBlueprint = Blueprint("currencyBlueprint", __name__, url_prefix='/currency')
currencyController = CurrencyController(db)
accountController = AccountController(db)

@currencyBlueprint.route("/", methods=['GET', 'OPTIONS'])
@currencyBlueprint.route("/<id>", methods=['GET', 'OPTIONS'])
@crossdomain(origin='*', headers=['x-access-token', 'Content-Type'])
@AuthenticatedUser
def GetCurrencies(id=None):
    if id != None:
        currency = currencyController.GetcurrencyBy(Id=id)
        if not currency or currency.UserId != request.user:
            return jsonify("currency not found"), 404
        return jsonify(currency.__serialize__())
    return jsonify(SerializeList(currencyController.GetAccountCurrencies(request.user)))

@currencyBlueprint.route("/", methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', headers=['x-access-token', 'Content-Type'])
@AuthenticatedUser
def AddNewCurrency():
    newCurrency = CurrencyDTO(**request.get_json())
    newCurrency.UserId = request.user
    if newCurrency.IsValid():
        newCurrencyId = currencyController.CreateCurrencyFromDTO(newCurrency)
        if not newCurrencyId:
            return jsonify("inserting new currency failed"), 400
        return jsonify(newCurrencyId), 200

@currencyBlueprint.route("/<id>", methods=['DELETE', 'OPTIONS'])
@crossdomain(origin='*', headers=['x-access-token', 'Content-Type'])
@AuthenticatedUser
def DeleteCurrency(id):
    success = currencyController.DeleteCurrency(id, request.user)
    if success:
        return jsonify("currency deleted"), 200
    return jsonify("failed to delete currency"), 400

