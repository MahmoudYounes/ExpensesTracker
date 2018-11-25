# TODO: refactor errors to always throw exceptions with message and error codes
# TODO: move all configuration to file
# TODO: create 
import sys, os, traceback

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

import Views

app = Flask(__name__)

# this should be read from an operating system environment variable
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ExpensesTrackerDBA:home0233308797@localhost/ExpensesTracker'
app.config['SECRET_KEY'] = 'precious'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
from Models.AccountModel import AccountModel
from Models.CategoryModel import CategoryModel
from Models.CurrencyModel import CurrencyModel
from Models.RecordModel import RecordModel
from Models.TokenModel import TokenModel

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# global exception filter. returning exception should not be supported 
@app.errorhandler(Exception)
def HandleExceptions(excep):
    exc_type, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)
    traceback.print_exc()
    return jsonify(str(excep)), 500

if __name__ == "__main__":
    app.register_blueprint(Views.adminBlueprint)
    app.register_blueprint(Views.accountBlueprint)
    app.register_blueprint(Views.authenticationBlueprint)
    app.register_blueprint(Views.recordBlueprint)
    app.register_blueprint(Views.currencyBlueprint)
    app.register_blueprint(Views.categoryBlueprint)
    manager.run()