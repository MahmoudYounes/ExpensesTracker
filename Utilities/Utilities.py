# must be deprecated
def ConstructDTOFromObjectModel(dtoClass, objModel):
    """
    constructs dto from set of model objects. supports lists
    """
    def _ConstructSingleDtoObject(dtoClass, objModel):
        newDto = dtoClass()
        for target in dtoClass.targets:
            setattr(newDto, target, getattr(objModel, target))
        return newDto
    if hasattr(objModel, '__iter__'):
        constructedObjects = []
        for obj in objModel:
            constructedObjects.append(_ConstructSingleDtoObject(dtoClass, obj))
        return constructedObjects
    else:
        return _ConstructSingleDtoObject(dtoClass, objModel)

# must be deprecated
def ConstructObjectModelFromDTO(objClass, dto):
    def _ConstructSingleObjectModel(objClass, dto):
        newModel = objClass()
        for target in dto.__class__.required:
            setattr(newModel, target, getattr(dto, target))
        return newModel
    if hasattr(dto, '__iter__'):
        constructedObjects = []
        for d in dto:
            constructedObjects.append(_ConstructSingleObjectModel(objClass, d))
        return constructedObjects
    else:
        return _ConstructSingleObjectModel(objClass, dto)

# must be deprecated 
def Serialize(objs):
    def _SerializeSingle(obj):
        if not hasattr(obj.__class__, '__serialize__'):
            raise ValueError("Internal Server Error")
        return obj.__serialize__()
    if hasattr(objs, '__iter__'):
        serialized = []
        for obj in objs:
            serialized.append(_SerializeSingle(obj))
        return serialized
    else:
        return _SerializeSingle(objs)


def SerializeDate(date):
    if date:
        return str(date)
    return None

def SerializeList(data):
    try:
        return [dataItem.__serialize__() for dataItem in data if hasattr(dataItem, '__serialize__')]
    except Exception as e:
        print(e)
        raise Exception("error occured at server.")

def IsValid(jsonObj, required):
    for req in required:
        if jsonObj.get(req, None) == None:
            return False
    return True