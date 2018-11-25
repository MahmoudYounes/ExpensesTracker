from flask import jsonify, Blueprint

from server import db
from wrappers import *
from Controllers import RecordController, RecordDTO
from Utilities import *


recordBlueprint = Blueprint("recordBlueprint", __name__, url_prefix='/record')
recordController = RecordController(db)

@recordBlueprint.route("/", methods=['GET', 'OPTIONS'])
@recordBlueprint.route("/<id>", methods=['GET', 'OPTIONS'])
@crossdomain(origin='*', headers=['x-access-token', 'Content-Type'])
@AuthenticatedUser
def GetRecords(id=None):
    if id != None:
        record = recordController.GetRecordInfo(id, request.user)
        if not record:
            return jsonify("record not found"), 404
        return jsonify(Serialize(record))
    return jsonify(Serialize(recordController.GetAccountRecords(request.user)))


@recordBlueprint.route("/", methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', headers=['x-access-token', 'Content-Type'])
@AuthenticatedUser
def AddNewRecord():
    newRecordDto = RecordDTO(**request.get_json())
    newRecordId = recordController.CreateRecordFromDTO(newRecordDto)
    if not newRecordId:
        return jsonify("failed to create record"), 400
    return jsonify(newRecordId)


@recordBlueprint.route("/", methods=['PUT', 'OPTIONS'])
@crossdomain(origin='*', headers=['x-access-token', 'Content-Type'])
@AuthenticatedUser
def UpdateRecord():
    if recordController.UpdateRecord(request.user, **request.get_json()):
        return jsonify("Done"), 200
    return jsonify("Error happened"), 500



@recordBlueprint.route("/<id>", methods=['DELETE', 'OPTIONS'])
@crossdomain(origin='*', headers=['x-access-token', 'Content-Type'])
@AuthenticatedUser
def DeleteRecord(id):
    success = recordController.DeleteRecord(id, request.user)
    if success:
        return jsonify("record deleted"), 200
    return jsonify("failed to delete record"), 400

