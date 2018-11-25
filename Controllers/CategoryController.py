from flask import request, g
from datetime import datetime, timedelta
import jwt

from werkzeug.security import generate_password_hash, check_password_hash

from Models import CategoryModel
from Utilities.Utilities import *

from server import app
from Utilities import *


class CategoryController:
    required = ['CategoryName', 'UserId']

    def __init__(self, db):
        self._db = db

    def GetCategoryBy(self, Id=None):
        targetCategory = None
        if Id:
            targetCategory = CategoryModel.query.filter_by(Id=Id).first()
        if targetCategory and not targetCategory.IsDeleted:
            return targetCategory
        else:
            return None
    
    def CreateCategoryFromJson(self, jsonObj):
        duplicateCategory = CategoryModel.query.filter_by(CategoryName=dto.CategoryName).first()
        if duplicateCategory and request.user == duplicateCategory.UserId:
            raise ValueError("There already exists a category with the same name.")
        
        if not IsValid(jsonObj, self.__class__.required):
            return None

        newCategory = CategoryModel(**jsonObj)
        self._db.session.add(newCategory)
        try:
            self._db.session.flush()
            self._db.session.commit()
        except Exception as e:
            print(e)
            self._db.session.rollback()
            return None
        return newCategory.CategoryId

    def GetAllCategories(self):
        allCategories = CategoryModel.query.all()
        return allCategories
    
    def GetAccountCategories(self, userId):
        allCategories = CategoryModel.query.filter_by(UserId=userId).all()
        return allCategories
    
    def DeleteCategory(self, id, userId):
        category = CategoryModel.query.filter_by(CategoryId=id, UserId=userId).first()
        if category == None:
            return False
        self._db.session.delete(category)
        self._db.session.commit()
        return True

class CategoryDTO:
    targets = ['CategoryId', 'CategoryName', 'CreatedAt', 'UserId']
    required = ['CategoryName', 'UserId']
    def __init__(self, **kwargs):
        self.CategoryName = kwargs.get('CategoryName', None)
        self.UserId = kwargs.get('UserId', None)

    def IsValid(self):
        for req in self.required:
            if getattr(self, req) == None:
                return False
        return True