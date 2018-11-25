def AssertNone(**kwargs):
    for key, val in kwargs.items():
        if val == None:
            return True
    return False

def ValidateId(Id):
    try:
        if Id == None:
            raise ValueError("Id cannot be None")
        idAsInt = int(Id)
        return idAsInt > 0
    except Exception as e:
        return False