from Controllers.AccountController import ExpensesTrackerAccountController, AccountModel

from server import db

import unittest

class TestExpensesTrackeraccountController(unittest.TestCase):
    def setUp(self):
        self.controller = ExpensesTrackerAccountController(db)
        self.addedUsers = []

    def test_CreateAccount(self):
        newUser = {'username':'TestingUser', 'password':'123456', 'email':'m.younesbadr@gmail.com', 'firstName':'wa7wa7', 'lastName':'ali', 'isAdmin':False, 'isStaff':False}
        addedUser = self.controller.CreateAccount(**newUser)
        self.addedUsers.append(addedUser)
        addedUser = AccountModel.query.filter_by(Id=addedUser).first()
        self.assertTrue(addedUser != None)

    def test_GetUserToken(self):
        newUser = {'username':'TestingUser', 'password':'123456', 'email':'m.younesbadr@gmail.com', 'firstName':'wa7wa7', 'lastName':'ali', 'isAdmin':False, 'isStaff':False}
        addedUser = self.controller.CreateAccount(**newUser)
        if not addedUser:
            print("failed to add user")
            assertTrue(False)
        self.addedUsers.append(addedUser)
        token = self.controller.GetUserToken("m.younesbadr@gmail.com", "123456")
        self.assertTrue(token != None)

    def tearDown(self):
        for user in self.addedUsers:
            userToDelete = AccountModel.query.filter_by(Id=user).first()
            db.session.delete(userToDelete)
            db.session.commit()        



        



