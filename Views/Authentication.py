from flask import request, jsonify, Blueprint

from server import db
from Controllers import AccountController, AccountDTO
from wrappers import crossdomain

accountController = AccountController(db)
authenticationBlueprint = Blueprint('authenticationBlueprint', __name__)

# TODO: add password strength validation

@authenticationBlueprint.route('/authenticate', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', headers=['x-access-token', 'Content-Type'])
def Login():
    requestData = request.get_json()
    email = requestData.get('email', None)
    password = requestData.get('password', None)
    if email == None or password == None:
        return jsonify("could not authenticate user. wrong email or password"), 200

    userToken = accountController.GetUserToken(email=email, password=password)
    if userToken:
        return jsonify(userToken.decode('UTF-8'))
    return jsonify("could not create token. please, try again later"), 400

@authenticationBlueprint.route('/signup', methods=['POST'])
@crossdomain(origin='*', headers=['x-access-token', 'Content-Type'])
def Signup():
    newAccountID = accountController.CreateAccountFromJson(request.get_json())
    if not newAccountID:
        return jsonify("Failed to create account"), 500
    return jsonify(newAccountID)

