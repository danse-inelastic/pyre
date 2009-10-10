

def getTypes(): return types


def addType(type): types.append(type)


def deleteType(type):
    if type not in types: return
    del types[types.index(type)]
    return


types = []
