from flask import request, jsonify, make_response, current_app
from functools import wraps, update_wrapper
import jwt

from datetime import timedelta

from server import app
from Models import AccountModel

def AuthenticatedUser(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return jsonify("can't authenticate token"), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            user = AccountModel.query.filter_by(email=data['email']).first()
            request.user = user.Id
        except Exception as e:
            print(e)
            return jsonify("can't authenticate token"), 401
        
        return func(*args, **kwargs)
    return decorated
 

def AuthorizedAdminUser(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify("can't authenticate token"), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            user = AccountModel.query.filter_by(email=data['email']).first()
            request.user = user.Id
        except Exception as e:
            print(e)
            return jsonify("can't authenticate token"), 401
        aUser = AccountModel.query.filter_by(Id=request.user).first()
        if not aUser.isSuperUser:
            return jsonify("Unauthorized user"), 401
        return func(*args, **kwargs)
    return decorated


def crossdomain(origin=None, methods=None, headers=None,
                maxAge=21600, attachToAll=True,
                automaticOptions=True):
    
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(maxAge, timedelta):
        maxAge = maxAge.total_seconds()

    def GetMethods():
        if methods is not None:
            return methods

        optionsResp = current_app.make_default_options_response()
        return optionsResp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automaticOptions and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attachToAll and request.method != 'OPTIONS':
                return resp

            header = resp.headers

            header['Access-Control-Allow-Origin'] = origin
            header['Access-Control-Allow-Methods'] = GetMethods()
            header['Access-Control-Max-Age'] = str(maxAge)
            if headers is not None:
                header['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator