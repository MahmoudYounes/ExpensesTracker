"""
for myself: why am I adding a DTO layer? because user income data has to pass by a validation layer 
    that way it is more secure.  a bit !
"""
from flask import jsonify, Blueprint, request

from server import db
from wrappers import *
from Controllers import CategoryController, CategoryDTO, AccountController
from Utilities import *


categoryBlueprint = Blueprint("categoryBlueprint", __name__, url_prefix='/category')
categoriesController = CategoryController(db)
accountController = AccountController(db)

@categoryBlueprint.route("/", methods=['GET', 'OPTIONS'])
@categoryBlueprint.route("/<id>", methods=['GET', 'OPTIONS'])
@crossdomain(origin='*', headers=['x-access-token', 'Content-Type'])
@AuthenticatedUser
def GetCategories(id=None):
    if id != None:
        category = categoriesController.GetCategoryBy(Id=id)
        if category.UserId != request.user:
            return jsonify("Category not found"), 404
        return jsonify(category.__serialize__())
    return jsonify(SerializeList(categoriesController.GetAccountCategories(request.user)))

@categoryBlueprint.route("/", methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', headers=['x-access-token', 'Content-Type'])
@AuthenticatedUser
def AddNewCategory():
    requestData = request.get_json()
    requestData['UserId'] = request.user
    newCategoryId = categoriesController.CreateCategoryFromJson(requestData)
    if not newCategoryId:
        return jsonify("inserting new category failed"), 400
    return jsonify(newCategoryId), 200

@categoryBlueprint.route("/<id>", methods=['DELETE', 'OPTIONS'])
@crossdomain(origin='*', headers=['x-access-token', 'Content-Type'])
@AuthenticatedUser
def DeleteCategory(id):
    success = categoriesController.DeleteCategory(id, request.user)
    if success:
        return jsonify("Category deleted"), 200
    return jsonify("failed to delete category"), 400

